/* global $ */

const handleDenyModal = function (modalElement, modalTitle, modalContent) {
  setModalTitle(modalElement, modalTitle)
  const modalBodyElement = modalElement.querySelector('.modal-body')
  modalBodyElement.innerHTML = modalContent
}

const setupModal = function (anchorId, deny) {
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
