document.addEventListener('DOMContentLoaded', function () {
  const submitBtn = document.querySelector('.btn-primary')
  const acceptTosCheckBox = document.getElementById('id_accepted_terms_of_service')
  submitBtn.disabled = !acceptTosCheckBox.checked
  acceptTosCheckBox.addEventListener('change', function () {
    submitBtn.disabled = !acceptTosCheckBox.checked
  })
})
