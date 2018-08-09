#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Compute aggregated emissions


Example usage
=============

>>> import profiles.models as pm
>>> import tracks.models as tm
>>> user = pm.SmbUser.objects.get(username="track_tester1")
>>> user_uuid = track_tester1.keycloak.UID

Emissions
---------

1. Total emissions by type of pollutant

   1. For all users

      >>> get_aggregated_data("emissions")

   2. For a single user

      1. By user instance

         >>> get_aggregated_data(
         ...     "emissions",
         ...     segment_filters={"track__owner": user})

      2. By username

         >>> get_aggregated_data(
         ...     "emissions",
         ...     segment_filters={"track__owner__username": user.username})

      3. By keycloak UUID

         >>> get_aggregated_data(
         ...     "emissions",
         ...     segment_filters={
         ...         "track__owner__keycloak__UID": user_uuid
         ...     }
         ... )
         >>> # alternative solution, using directly the Segment.user_uuid field
         >>> get_aggregated_data(
         ...     "emissions", segment_filters={"user_uuid": user_uuid})


2. Total emissions by type of pollutant and vehicle type for all users

   1. For all users

   >>> get_annotated_emissions(annotate_by=["vehicle_type"])

   2. For a single user (can also use username, keycloak UUID, etc)

   >>> get_annotated_emissions(
   ...     annotate_by=["vehicle_type"],
   ...     segment_filters={"track__owner": user}
   ... )


3. Total emissions by type of pollutant and age range

   >>> get_annotated_emissions(
   ...     annotate_by=["track__owner__enduserprofile__age"],
   ... )


4. Total emissions by type of pollutant and by occupation type of the user

   >>> get_annotated_emissions(
   ...     annotate_by=["track__owner__enduserprofile__occupation"])


5. Total emissions by type of pollutant and by hour range (0-6, 6-12,
   12-18, 18-24)

   TODO


6. Total saved emissions by type of pollutant - See 1., the results include
   both emitted and saved emissions


7. Total saved emissions by type of pollutant and by vehicle_type - See 2., the
   results include both emitted and saved emissions


Costs
-----

8. Total costs to move

   1. For all users

      >>> get_aggregated_data("costs")

   2. For a single user

      >>> get_aggregated_data(
      ...     "costs",
      ...     segment_filters={"track__owner": user})


9. Total costs by class of cost - See 8., the results include total costs and
   also the cost for each class


10. Total costs by vehicle type (only for motorbike, car and bus)

    >>> get_annotated_costs(
    ...     annotate_by=["vehicle_type"]
    ... ).filter(vehicle_type__in=[tm.BUS, tm.CAR, tm.MOTORBIKE])


11. Total costs by age range of the user

    >>> get_annotated_costs(annotate_by=["track__owner__enduserprofile__age"])


12. Total costs by occupation type of the user

    >>> get_annotated_costs(
    ...     annotate_by=["track__owner__enduserprofile__occupation"])


13. Total costs by hour range (0-6, 6-12, 12-18, 18-24)

   TODO


Calories consumption
--------------------

14. Total calories consumed

   1. For all users

      >>> get_aggregated_data("health")

   2. For a single user

      >>> get_aggregated_data(
      ...     "health",
      ...     segment_filters={"track__owner": user})



15. Total calories by vehicle type (foot or bike)

    >>> get_annotated_health(
    ...    annotate_by=["vehicle_type"]
    ... ).filter(vehicle_type__in=[tm.BIKE, tm.FOOT])


16. Total calories by age range of the user

    >>> get_annotated_health(
    ...    annotate_by=["track__owner__enduserprofile__age"]
    ... )


17. Total calories by occupation type of the user

    >>> get_annotated_health(
    ...    annotate_by=["track__owner__enduserprofile__occupation"]
    ... )


18. Total calories by hour range (0-6, 6-12, 12-18, 18-24)

    TODO

"""

from django.db.models import Sum

from . import models


def get_aggregated_data(data_type, annotate_by=None, segment_filters=None,
                        annotation_function=Sum, aggregation_function=Sum):
    annotation_handler, aggregation_functions_handler = {
        "emissions": (
            get_annotated_emissions,
            get_emission_aggregation_functions
        ),
        "costs": (
            get_annotated_costs,
            get_cost_aggregation_functions
        ),
        "health": (
            get_annotated_health,
            get_health_aggregation_functions
        ),
    }.get(data_type)
    prefix = "temp_"
    qs = annotation_handler(
        annotate_by=annotate_by,
        segment_filters=segment_filters,
        annotation_prefix=prefix,
        annotation_function=annotation_function
    )
    aggregation_functions = aggregation_functions_handler(
        lookup_pattern="{}{{}}".format(prefix),
        annotation_function=aggregation_function
    )
    return qs.aggregate(**aggregation_functions)


def get_annotated_health(annotate_by=None, segment_filters=None,
                         annotation_prefix="", annotation_function=Sum):
    aggregation_functions = get_health_aggregation_functions(
        lookup_pattern="health__{}",
        name_prefix=annotation_prefix,
        annotation_function=annotation_function
    )
    return _get_annotated_segment_data(
        aggregation_functions,
        annotate_by=annotate_by,
        segment_filters=segment_filters,
    )


def get_annotated_emissions(annotate_by=None, segment_filters=None,
                            annotation_prefix="", annotation_function=Sum):
    aggregation_functions = get_emission_aggregation_functions(
        lookup_pattern="emission__{}",
        name_prefix=annotation_prefix,
        annotation_function=annotation_function
    )
    return _get_annotated_segment_data(
        aggregation_functions,
        annotate_by=annotate_by,
        segment_filters=segment_filters,
    )


def get_annotated_costs(annotate_by=None, segment_filters=None,
                        annotation_prefix="", annotation_function=Sum):
    aggregation_functions = get_cost_aggregation_functions(
        lookup_pattern="cost__{}",
        name_prefix=annotation_prefix,
        annotation_function=annotation_function
    )
    return _get_annotated_segment_data(
        aggregation_functions,
        annotate_by=annotate_by,
        segment_filters=segment_filters,
    )


def _get_annotated_segment_data(annotations, annotate_by=None,
                                segment_filters=None):
    annotate_by = list(annotate_by) if annotate_by is not None else []
    qs = models.Segment.objects.values(*annotate_by)
    filters_ = dict(segment_filters) if segment_filters is not None else {}
    qs = qs.filter(**filters_)
    qs = qs.annotate(**annotations)
    return qs


def get_emission_aggregation_functions(lookup_pattern, name_prefix="",
                                       annotation_function=Sum):
    field_names = [
        "so2",
        "so2_saved",
        "nox",
        "nox_saved",
        "co2",
        "co2_saved",
        "co",
        "co_saved",
        "pm10",
        "pm10_saved",
    ]
    return _get_segment_data_aggregation_functions(
        lookup_pattern,
        field_names=field_names,
        name_prefix=name_prefix,
        aggregation_function=annotation_function
    )


def get_cost_aggregation_functions(lookup_pattern, name_prefix="",
                                   annotation_function=Sum):
    field_names = [
        "fuel_cost",
        "time_cost",
        "depreciation_cost",
        "operation_cost",
        "total_cost",
    ]
    return _get_segment_data_aggregation_functions(
        lookup_pattern,
        field_names=field_names,
        name_prefix=name_prefix,
        aggregation_function=annotation_function
    )


def get_health_aggregation_functions(lookup_pattern, name_prefix="",
                                     annotation_function=Sum):
    field_names = [
        "calories_consumed",
        "benefit_index",
    ]
    return _get_segment_data_aggregation_functions(
        lookup_pattern,
        field_names=field_names,
        name_prefix=name_prefix,
        aggregation_function=annotation_function
    )


def _get_segment_data_aggregation_functions(lookup_pattern,
                                            field_names,
                                            name_prefix="",
                                            aggregation_function=Sum):
    names = ["{}{}".format(name_prefix, i) for i in field_names]
    annotations = {}
    for annotation_name, lookup in zip(names, field_names):
        annotations[annotation_name] = aggregation_function(
            lookup_pattern.format(lookup))
    return annotations
