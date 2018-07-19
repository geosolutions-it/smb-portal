/* global toggleUploadButton */

document.addEventListener('DOMContentLoaded', function () {
  const fileInputElement = document.getElementById('id_image')
  const submitBtn = document.querySelector('.btn-primary')
  toggleUploadButton(submitBtn, fileInputElement)

  fileInputElement.addEventListener('change', function (evt) {
    toggleUploadButton(submitBtn, evt.target)
  })
})
