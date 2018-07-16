document.addEventListener('DOMContentLoaded', function () {
  const submitBtn = document.querySelector('.btn-primary')
  const acceptTosCheckBox = document.getElementById('id_accepted_terms_of_service')
  submitBtn.disabled = !acceptTosCheckBox.checked
  acceptTosCheckBox.addEventListener('change', function () {
    submitBtn.disabled = !acceptTosCheckBox.checked
  })
  // This is a hack to move the `accepted_terms_of_service` checkbox to the
  // bottom of the form. It works by moving the element to the end of the form
  // and then moving also the submit button to the end.
  //
  // This hack is here because django is autogenerating the markup for this
  // page and it is using three different forms. The
  // `accepted_terms_of_service` checkbox is part of the `user` form, which is
  // the first to be rendered.
  if (window.location.pathname.split('/').pop() === 'create') {
    const acceptTosCheckBoxParent = acceptTosCheckBox.parentNode.parentNode.parentNode
    const formElement = acceptTosCheckBoxParent.parentNode
    formElement.appendChild(acceptTosCheckBoxParent)
    formElement.appendChild(submitBtn)
  }
})
