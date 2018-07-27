/* global setupModal */
/* global toggleUploadButton */
/* global validateAddition */

const toggleUpload = function () {
  const fileInputElement = document.getElementById('id_image')
  const submitBtn = document.querySelector('.btn-primary')
  toggleUploadButton(submitBtn, fileInputElement)

  fileInputElement.addEventListener('change', function (evt) {
    toggleUploadButton(submitBtn, evt.target)
  })
}

setupModal('addPicture', !validateAddition('addPicture'), toggleUpload)
