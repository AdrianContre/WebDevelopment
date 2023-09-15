document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  //handle compose submit
  document.querySelector('#compose-form').onsubmit = sendEmail;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      let li = document.createElement('div');
      if (email.read) {
        li.style.backgroundColor = "gray";
      }
      else li.style.backgroundColor = "white";
      li.style.borderColor = "black";
      li.className = "list-group-item";
      li.innerHTML = `
      <p><strong>To:</strong> ${email.recipients[0]}</p>
      <p><strong>Subject:</strong> ${email.subject} </p>
      <p><strong>Timestamp:</strong> ${email.timestamp} </p>
      `;
      document.querySelector('#emails-view').append(li);
      li.addEventListener('click',() => loadEmail(email.id,mailbox));
    })
  });
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function sendEmail() {
  //First,we take the values of the form
  const recipient = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  //Now,we make a post request
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipient,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    load_mailbox('sent');
    console.log(result);
  });

  //event prevent default
  return false;
}

function loadEmail(emailId,mailbox) {
  const container = document.querySelector('#email-view');
  removeAllChildNodes(container)
  //set email as read
  fetch(`/emails/${emailId}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  fetch(`/emails/${emailId}`)
  .then(response => response.json())
  .then(email => {
    //Hide the elements of view-emails
    let view = document.querySelector('#emails-view');
    view.style.display = 'none';

    const emailDisplayed = document.createElement('div');
    emailDisplayed.className = "list-group-item";
    emailDisplayed.innerHTML = `
    <p><strong>From:</strong> ${email.sender} </p>
    <p><strong>To:</strong> ${email.recipients[0]}</p>
    <p><strong>Subject:</strong> ${email.subject} </p>
    <p><strong>Timestamp:</strong> ${email.timestamp} </p>
    `
    if (mailbox != 'sent') {
      const archiveButton = document.createElement('button');
      archiveButton.className ="btn btn-sm btn-outline-primary"
      if (email.archived) {
        archiveButton.innerHTML = "Unarchive"
      }
      else {
        archiveButton.innerHTML = "Archive"
      }
      const replyButton = document.createElement('button');
      replyButton.innerHTML = "Reply";
      replyButton.className = "btn btn-sm btn-outline-primary";
      const buttonGroupDiv = document.createElement('div');
      buttonGroupDiv.appendChild(replyButton);
      buttonGroupDiv.appendChild(archiveButton);
      emailDisplayed.insertBefore(buttonGroupDiv, emailDisplayed.querySelector("hr"));
      emailDisplayed.insertAdjacentHTML("beforeend", `<hr><p>${email.body}</p>`);
      document.querySelector('#email-view').append(emailDisplayed);
      archiveButton.addEventListener('click', () => archiveMail(emailId,archiveButton.innerHTML));
      replyButton.addEventListener('click', () => replyEmail(emailId));

    }
    else {
      emailDisplayed.insertAdjacentHTML("beforeend", `<hr><p>${email.body}</p>`);
      document.querySelector('#email-view').append(emailDisplayed);
    }

    document.querySelector('#email-view').style.display = 'block';

    


  }); 
}


function archiveMail(emailId,type) {
  let bool;
  if (type === "Archive") {
    bool = true;
  }
  else bool = false;
  fetch(`/emails/${emailId}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: bool
    })
  })
  .then(email => {
    load_mailbox('inbox')
  });
}

function replyEmail(emailId) {
  fetch(`/emails/${emailId}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#email-view').style.display = 'none';
    
    //Fill the desired fields
    document.querySelector('#compose-recipients').value = email.sender;
    if ((email.subject).startsWith('Re:')) {
      document.querySelector('#compose-subject').value = email.subject;
    }
    else {
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    }
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:
${email.body}
    `;

  });
  return false;

}


//removes all the childs from a parent container of html
function removeAllChildNodes(parent) {
  while (parent.firstChild) {
    parent.removeChild(parent.firstChild);
  }
}

