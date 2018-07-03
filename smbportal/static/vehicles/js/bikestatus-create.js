document.addEventListener('DOMContentLoaded', function (evt) {
  const pathList = window.location.pathname.split('/')
  const bikesPosition = pathList.findIndex(item => item === 'bikes')
  const isStatusSection = pathList[bikesPosition + 1] === 'report-status'
  const highlightId = (isStatusSection ? 'reportLost' : 'bikes')
  document.getElementById(highlightId).classList.add('active')
})
