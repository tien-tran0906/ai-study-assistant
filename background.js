// const getResponse = async (question) => {
//   return new Promise(async (resolve, reject) => {
//     try {
//       const res = await fetch(
//         'https://chat.openai.com/backend-api/conversation',
//         {
//           method: 'POST',
//           headers: {
//             'Content-Type': 'application/json',
//           },
//           body: JSON.stringify({
//             action: 'next',
//             messages: [
//               {
//                 id: uid(),
//                 role: 'user',
//                 content: {
//                   content_type: 'text',
//                   parts: [question],
//                 },
//               },
//             ],
//             model: 'text-davinci-002-render',
//             parent_message_id: uid(),
//           }),
//         }
//       );
//       resolve(res.body);
//     } catch (e) {
//       reject('ERROR');
//     }
//   });
// };

// chrome.runtime.onConnect.addListener((port) => {
//   port.onMessage.addListener((msg) => {
//     const question = msg.selectedText;
//     getResponse(question)
//       .then(async (answer) => {
//         const resRead = answer.getReader();
//         while (true) {
//           const { done, value } = await resRead.read();
//           if (done) break;
//           if (done === undefined || value === undefined)
//             port.postMessage('ERROR');
//           const data = new TextDecoder().decode(value);
//           port.postMessage(data);
//         }
//       })
//       .catch((e) => port.postMessage(e));
//   });
// });

// Background script is necessary for message passing between popup and content script

const returnSelection = () => {
  return new Promise((resolve, reject) => {
    if (window.getSelection) {
      resolve(window.getSelection().toString());
    } else if (document.getSelection) {
      resolve(document.getSelection().toString());
    } else if (document.selection) {
      resolve(document.selection.createRange().text.toString());
    } else reject();
  });
};

chrome.runtime.onMessage.addListener(async (request, sender, response) => {
  const { action } = request;
  if (action === 'getSelectedText') {
    try {
      const selectedText = await returnSelection();
      response({
        action: 'getSelectedTextResponse',
        selectedText: selectedText,
      });
    } catch (e) {
      response();
    }
  }
});
