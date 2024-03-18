// document.addEventListener('DOMContentLoaded', async () => {
//   const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

//   const getActiveTab = async () => {
//     const tabs = await chrome.tabs.query({
//       currentWindow: true,
//       active: true,
//     });
//     return tabs[0];
//   };

//   const showPopup = async (answer) => {
//     if (answer !== 'CLOUDFLARE' && answer !== 'ERROR') {
//       try {
//         let res = await answer.split('data:');
//         try {
//           const detail = JSON.parse(res[0]).detail;
//           document.getElementById('output').style.opacity = 1;
//           document.getElementById('output').innerHTML = detail;
//           return;
//         } catch (e) {
//           try {
//             res = res[1].trim();
//             if (res === '[DONE]') return;
//             answer = JSON.parse(res);
//             let final = answer.message.content.parts[0];
//             final = final.replace(/\n/g, '<br>');
//             document.getElementById('output').style.opacity = 1;
//             document.getElementById('output').innerHTML = final;
//           } catch (e) {}
//         }
//       } catch (e) {
//         document.getElementById('output').style.opacity = 1;
//         document.getElementById('output').innerHTML =
//           'Something went wrong. Please try in a few minutes.';
//       }
//     } else if (answer === 'CLOUDFLARE') {
//       document.getElementById('input').style.opacity = 1;
//       document.getElementById('input').innerHTML =
//         'You need to once visit <a target="_blank" href="https://chat.openai.com/chat">chat.openai.com</a> and check if the connection is secure. Redirecting...';
//       await sleep(3000);
//       chrome.tabs.create({ url: 'https://chat.openai.com/chat' });
//     } else {
//       document.getElementById('output').style.opacity = 1;
//       document.getElementById('output').innerHTML =
//         'Something went wrong. Are you logged in to <a target="_blank" href="https://chat.openai.com/chat">chat.openai.com</a>? Try logging out and logging in again.';
//     }
//   };

//   const getData = async (selection) => {
//     if (!selection.length == 0) {
//       document.getElementById('input').style.opacity = 1;
//       document.getElementById('input').innerHTML = selection;
//       document.getElementById('output').style.opacity = 0.5;
//       document.getElementById('output').innerHTML = 'Loading...';
//       const port = chrome.runtime.connect();
//       port.postMessage({ question: selection });
//       port.onMessage.addListener((msg) => showPopup(msg));
//     } else {
//       document.getElementById('input').style.opacity = 0.5;
//       document.getElementById('input').innerHTML =
//         'You have to first select some text';
//     }
//   };

//   const getSelectedText = async () => {
//     const activeTab = await getActiveTab();
//     chrome.tabs.sendMessage(activeTab.id, { type: 'LOAD' }, getData);
//   };

//   getSelectedText();
// });

//  ================================================================================== //
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
