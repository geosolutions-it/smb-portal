/* global ol */
/* global observationsUrl */

const observationsSource = new ol.source.Vector({
  url: observationsUrl,
  format: new ol.format.GeoJSON()
})

observationsSource.on('change', function (evt) {
  if (observationsSource.getState() === 'ready') {
    const view = map.getView()
    // recenter map based on loaded data's extent
    view.fit(this.getExtent(), {
      size: map.getSize(),
      padding: [5, 5, 5, 5]
    })
    // setup event listeners for listgroup items
    const observationElements = document.getElementsByName('observation')
    for (const observationElement of observationElements) {
      const observationId = Number(observationElement.id.split('-').pop())
      const feature = this.getFeatureById(observationId)
      observationElement.addEventListener('click', function () {
        view.animate({
          center: feature.getGeometry().getCoordinates(),
          zoom: view.getZoom() + 1,
          duration: 500
        })
      })
      observationElement.addEventListener('pointerover', function (evt) {
        const currentlySelected = observationSelect.getFeatures()
        currentlySelected.push(feature)
      })
      observationElement.addEventListener('pointerout', function (evt) {
        const currentlySelected = observationSelect.getFeatures()
        currentlySelected.clear()
      })
    }
  }
})

const observationFill = new ol.style.Fill({
  color: 'rgba(255, 0, 0, 0.5)'
})

const observationStyle = new ol.style.Style({
  image: new ol.style.Circle({
    radius: 5,
    fill: observationFill
  }),
  fill: observationFill
})

const map = new ol.Map({
  target: 'bike-map',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM()
    }),
    new ol.layer.Vector({
      source: observationsSource,
      style: observationStyle
    })
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([37.41, 8.82]),
    zoom: 4
  })
})

const observationSelect = new ol.interaction.Select({
  condition: ol.events.condition.pointerMove
})

observationSelect.on('select', function (evt) {
  const selectedFeatureIds = []
  for (const feature of evt.selected) {
    selectedFeatureIds.push(feature.getId())
  }

  for (const observationElement of document.getElementsByName('observation')) {
    const elementObservationId = Number(observationElement.id.split('-').pop())
    if (selectedFeatureIds.includes(elementObservationId)) {
      observationElement.classList.add('active')
    } else {
      observationElement.classList.remove('active')
    }
  }
})

map.addInteraction(observationSelect)
