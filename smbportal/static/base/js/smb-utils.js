/* global $ */

const setupSmbModalDisplay = function (anchorId) {
  document.getElementById(anchorId).addEventListener('click', function () {
    const modalAttrs = getDataAttrsDisplay('#' + anchorId)
    console.log('modalAttrs: ' + modalAttrs)
    setModalTitle(modalAttrs.title)
    loadDataIntoModalBody(modalAttrs.url)
  })
}

const getDataAttrsDisplay = function (anchorSelector) {
  return {
    title: document.querySelector(anchorSelector).dataset.title,
    url: document.querySelector(anchorSelector).dataset.contentsUrl,
  }
}

const loadDataIntoModalBody = function (url) {
  const primaryButtonElement = document.querySelector(
    '#smbModal .modal-footer #primaryButton')
  primaryButtonElement.parentElement.removeChild(primaryButtonElement)
  $('#smbModal .modal-dialog .modal-content .modal-body').load(url)
}


const setupSmbModal = function (anchorId) {
  document.getElementById(anchorId).addEventListener('click', function () {
    const modalAttrs = getDataAttrs('#' + anchorId)
    setModalTitle(modalAttrs.title)
    updateModalPrimaryButton(
      modalAttrs.primary.value,
      modalAttrs.primary.iconClasses,
      modalAttrs.primary.classes
    )
    loadFormIntoModalBody(modalAttrs.formAction)
  })
}

const updateModalPrimaryButton = function (text, iconClasses, buttonClasses) {
  const primaryButtonElement = document.querySelector(
    '#smbModal .modal-footer #primaryButton')
  primaryButtonElement.classList.add('btn-primary')
  primaryButtonElement.setAttribute('class', buttonClasses)
  const iElement = document.createElement('i')
  iElement.setAttribute('class', iconClasses)
  const primaryButtonText = document.createTextNode(' ' + text)
  while (primaryButtonElement.firstChild) {
    primaryButtonElement.firstChild.remove()
  }
  primaryButtonElement.appendChild(iElement)
  primaryButtonElement.appendChild(primaryButtonText)
  return primaryButtonElement
}

const getDataAttrs = function (anchorSelector) {
  return {
    title: document.querySelector(anchorSelector).dataset.title,
    formAction: document.querySelector(anchorSelector).dataset.actionUrl,
    primary: {
      classes: document.querySelector(anchorSelector).dataset.primaryButtonClasses,
      iconClasses: document.querySelector(anchorSelector).dataset.primaryButtonIcon,
      value: document.querySelector(anchorSelector).dataset.primaryButtonValue
    }
  }
}

const setModalTitle = function (title) {
  const modalTitleElement = document.querySelector('#smbModal .modal-title')
  modalTitleElement.textContent = title
}

const loadFormIntoModalBody = function (formAction) {
  const primaryButtonElement = document.querySelector(
    '#smbModal .modal-footer #primaryButton')
  console.log('primaryButtonElement: ' + primaryButtonElement)
  $('#smbModal .modal-dialog .modal-content .modal-body').load(
    formAction,
    null,
    function () {
      const loadedFormElement = document.querySelector(
        '#smbModal .modal-body form')
      primaryButtonElement.setAttribute('form', loadedFormElement.id)
    }
  )
}
