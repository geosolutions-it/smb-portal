/* global $ */

const handleDenyModal = function (modalElement, modalTitle, modalContent) {
  setModalTitle(modalElement, modalTitle)
  const modalBodyElement = modalElement.querySelector('.modal-body')
  modalBodyElement.innerHTML = modalContent
}

const setupModal = function (anchorId, deny, ajaxLoadedCallback) {
  const anchorElement = document.getElementById(anchorId)
  const dataAttrs = {
    title: anchorElement.dataset.title,
    formAction: anchorElement.dataset.actionUrl,
    primary: {
      classes: anchorElement.dataset.primaryButtonClasses,
      iconClasses: anchorElement.dataset.primaryButtonIcon,
      value: anchorElement.dataset.primaryButtonValue
    },
    denial: {
      title: anchorElement.dataset.denialTitle,
      content: anchorElement.dataset.denialContent
    }
  }
  let modalId = 'smbFormModal'
  if (deny) {
    modalId = 'smbDisplayModal'
    handleDenyModal(
      document.getElementById(modalId),
      dataAttrs.denial.title,
      dataAttrs.denial.content
    )
  } else {
    anchorElement.addEventListener('click', function () {
      const modalElement = document.getElementById(modalId)
      const primaryButtonElement = updateButton(
        modalElement.querySelector('#primaryButton'),
        dataAttrs.primary.value,
        dataAttrs.primary.iconClasses,
        dataAttrs.primary.classes
      )
      setModalTitle(modalElement, dataAttrs.title)
      const modalBodyElement = modalElement.querySelector('.modal-body')
      $(modalBodyElement).load(
        dataAttrs.formAction,
        null,
        function () {
          const loadedFormElement = modalBodyElement.querySelector('form')
          primaryButtonElement.setAttribute('form', loadedFormElement.id)
          if (ajaxLoadedCallback !== undefined) {
            ajaxLoadedCallback()
          }
        }
      )
    })
  }
  anchorElement.setAttribute('href', `#${modalId}`)
}

const setupModalDisplay = function (dataElement) {
  const dataAttrs = {
    title: dataElement.dataset.title,
    url: dataElement.dataset.contentsUrl
  }
  const modalElement = document.getElementById('smbDisplayModal')
  dataElement.addEventListener('click', function () {
    setModalTitle(modalElement, dataAttrs.title)
    const modalBodyElement = modalElement.querySelector('.modal-body')
    $(modalBodyElement).load(dataAttrs.url)
  })
}

const updateButton = function (button, text, iconClasses, buttonClasses) {
  button.setAttribute('class', buttonClasses)
  const iElement = document.createElement('i')
  iElement.setAttribute('class', iconClasses)
  const primaryButtonText = document.createTextNode(' ' + text)
  while (button.firstChild) {
    button.firstChild.remove()
  }
  button.appendChild(iElement)
  button.appendChild(primaryButtonText)
  return button
}

const setModalTitle = function (modalElement, title) {
  const modalTitleElement = modalElement.querySelector('.modal-title')
  modalTitleElement.textContent = title
}

const validateAddition = function (anchorId) {
  const anchorElement = document.querySelector(`#${anchorId}`)
  const threshold = Number(anchorElement.dataset.threshold)
  const current = Number(anchorElement.dataset.current)
  let result = true
  if (current >= threshold) {
    console.log('cannot add more objects')
    result = false
  }
  return result
}

const validateUploadSize = function (inputId) {
  const inputElement = document.getElementById(inputId)
  let result = false
  if (inputElement !== null) {
    const fileToUpload = inputElement.files.item(0)
    if (fileToUpload !== null) {
      const maxSize = Number(inputElement.dataset.uploadMaxSizeMegabytes)
      const sizeMegabytes = fileToUpload.size / 1000000
      if (sizeMegabytes <= maxSize) {
        result = true
      }
    }
  }
  return result
}

/**
 * Highlight the relevant menu item
 * @param {string} elementId
 */
const highlightMenuItem = function (elementId) {
  document.addEventListener('DOMContentLoaded', function (evt) {
    document.getElementById(elementId).classList.add('active')
  })
}

/**
 * Toggle the upload button if the selected file is too big
 * @param submitButtonElement
 * @param fileInputElement
 */
const toggleUploadButton = function (submitButtonElement, fileInputElement) {
  const okText = fileInputElement.dataset.successMessage
  const okIconClasses = fileInputElement.dataset.successIconClasses
  const koText = fileInputElement.dataset.errorMessage
  const koIconClasses = fileInputElement.dataset.errorIconClasses
  while (submitButtonElement.firstChild) {
    submitButtonElement.firstChild.remove()
  }

  const iElement = document.createElement('i')
  submitButtonElement.append(iElement)
  const textNode = document.createTextNode('')

  if (!validateUploadSize(fileInputElement.id)) {
    submitButtonElement.disabled = true
    if (fileInputElement.files.length === 0) {
      iElement.setAttribute('class', okIconClasses)
      textNode.textContent = ` ${okText}`
    } else {
      iElement.setAttribute('class', koIconClasses)
      textNode.textContent = ` ${koText}`
    }
  } else {
    submitButtonElement.disabled = false
    iElement.setAttribute('class', okIconClasses)
    textNode.textContent = ` ${okText}`
  }
  submitButtonElement.append(iElement)
  submitButtonElement.append(textNode)
}
