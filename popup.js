document.addEventListener('DOMContentLoaded', function () {
  var linkGeneratorButton = document.getElementById('link-generator');
  var outputFileName = document.getElementById('output-file-name');
  var inputText = document.getElementById('input');
  var outputLink = document.getElementById('output-link');
  var loadingGif = document.getElementById('loading-gif');
  var copyRightElement = document.getElementById('gif-copyright')
  var loading = document.getElementById('loading')

  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    chrome.tabs.sendMessage(
      tabs[0].id,
      { action: 'getSelectedText', type: 'LOAD' },
      function (response) {
        inputText.innerText = response.selectedText;
      }
    );
  });

  linkGeneratorButton.addEventListener('click', function () {
    var fileName = outputFileName.value.trim();
    if (fileName !== '') {
      // loadingGif.style.display = 'block';
      loading.style.display = 'block';
      copyRightElement.style.display = 'block';
      var dataToSend = {
        action: 'generateLink',
        context: inputText.innerText,
        fileName: fileName,
      };
      sendDataToAPI(dataToSend, function (result) {
        console.log(result)
        loadingGif.style.display = 'none';
        loading.style.display = 'none';
        copyRightElement.style.display = 'none';
        outputLink.innerHTML =
          '<a href="' + result.doc_url + '" target="_blank">' + result.doc_url + '</a>';
      });
    } else {
      outputLink.innerHTML = 'Please enter a valid file name.';
    }
  });

  function sendDataToAPI(data, callback) {
    // Replace 'YOUR_API_ENDPOINT' with your actual API endpoint
    var apiEndpoint = 'http://127.0.0.1:8000';
    var xhr = new XMLHttpRequest();
    xhr.open('POST', apiEndpoint, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          var response = JSON.parse(xhr.responseText);
          callback(response);
        } else {
          console.error('Error:', xhr.statusText);
        }
      }
    };
    xhr.send(JSON.stringify(data));
  }
});
