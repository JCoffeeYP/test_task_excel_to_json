const form = document.querySelector('#form')

form.onsubmit = async (e) => {
  e.preventDefault();

  let response = await fetch('/upload/excel', {
    method: 'POST',
    body: new FormData(form)
  });
  try {
    let result = await response.json();
    getStatus(result.task_id)
  }
  catch (e) {
    alert('Ошибка ' + e.name + ":" + e.message + "\n" + e.stack);
  }
};

function getStatus(taskID) {
  fetch(`/upload/excel/${taskID}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  })
  .then(response => response.json())
  .then(res => {
    console.log(res)
    const html = `
      <tr>
        <td>${taskID}</td>
        <td>${res.task_status}</td>
      </tr>`;
    const newRow = document.getElementById('tasks').insertRow(0);
    newRow.innerHTML = html;

    const taskStatus = res.task_status;
    if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') return false;
    setTimeout(function() {
      getStatus(res.task_id);
    }, 10000);
  })
  .catch(err => console.log(err));
}