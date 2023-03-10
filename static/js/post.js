const contentInput = document.getElementById("id_content");
const contentDiv = document.getElementById("post_content");

// switch the current value for the content input and the custom div content editable
if (contentDiv) {
  contentDiv.addEventListener("input", switchContent);
}

// befor update fill the current value to content input to the content div editable
const updatePostContent = document.querySelector(".update_post");
if (updatePostContent) {
  contentDiv.textContent = contentInput.value;
}

// get the current csrf_token value
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

csrftoken = getCookie("csrftoken");

// send asynchronous comment value to the backend
let commentBtn = document.getElementById("submit_comment");
if (commentBtn) {
  commentBtn.addEventListener("click", send_data);
}

function isEmptyFieldValue(ele) {
  // if the comment body is empty
  return ele.get("body") === "";
}

async function send_data(e) {
  e.preventDefault();
  //   grab and create new form data
  let formData = new FormData(comment_form);

  // change the current checkbox value
  if (formData.has("active")) {
    formData.get("active") === "on"
      ? formData.set("active", "True")
      : formData.set("active", "False");
  }

  //  create a json format of the formData
  let keys = ["username", "email", "body", "active"];
  let datas = {};
  keys.forEach((key) => {
    if (formData.has(key)) datas[key] = formData.get(key);
  });

  post_data = {
    method: "POST",
    credentials: "same-origin",
    headers: {
      Accept: "application/json",
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(datas),
  };

  let checker = document.getElementById("comment_checker");

  if (!isEmptyFieldValue(formData)) {
    const response = await fetch(document.URL, post_data);
    const data = await response.json();
    let comment = document.getElementById("post_comment");
    let htmlFragment = createHtmlFragment(data["post_comment"]);
    comment.insertAdjacentHTML("beforeend", htmlFragment);

    // update the current total number of comments
    document.getElementById("num_comments").textContent =
      data["comment_number"];
  } else {
    checker.classList.add("active");
  }
}

function createHtmlFragment(post) {
  let htmlFragment = `
          <div class="post_comment">
              <span>${post.username}</span>
              <span>${post.email}</span>
              <span>Comment at:${new Date(Date.now())}</span>
              <p>${post.body}</p>
          </div>
          `;
  return htmlFragment;
}



// subscription part
let checker = document.getElementById("valid_action");

let subscribeForm = document.getElementById("subscribe");
if (subscribeForm) {
  checker.hidden = true;
  let url = subscribeForm.action;
  let data = { email: document.getElementById("sub_email").value };
  subscribeForm.addEventListener("submit", (e) => {
    e.preventDefault();

    post_data = {
      method: "POST",
      credentials: "same-origin",
      headers: {
        Accept: "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify(data),
    };
    fetch(url, post_data).then((data) => {
      if (data.ok && data.status === 200) {
        checker.hidden = false;
        document.querySelector(".subscribe__container").hidden = true;
      }
    });
  });
}

// toggle comment and share section

let currentComment = document.getElementById("comment");
let switchComment = document.getElementById("id_body");

if (currentComment) {
  currentComment.addEventListener("input", switchContent);
}

let currentShare = document.getElementById("share_id");
let switchShare = document.getElementById("id_comment");

if (currentShare) {
  currentShare.addEventListener("input", switchContent);
}

// reset field  values on document on load
document.addEventListener("DOMContentLoaded", () => {
  if (switchShare) {
    resetFieldValue(switchShare);
  }
  if (switchComment) {
    resetFieldValue(switchComment);
  }
});

function resetFieldValue(field) {
  field.value = "";
}

// switch content

function switchContent(e) {
  let currentEle = e.target;
  switch (e.target.attributes.name.textContent) {
    case "create_post":
      switchEle = contentInput;
      break;

    case "share_post":
      switchEle = switchShare;
      break;

    case "comment_post":
      switchEle = switchComment;
      break;
  }
  switchText(currentEle, switchEle);
}

function switchText(currentEle, switchEle) {
  switchEle.value = currentEle.textContent;
  console.log(switchEle)
  console.log(currentEle);
  return switchEle.value;
}

// scrool to specific part of the detail post
let scrolDiv = document.querySelector(".scrol_links");

if(scrolDiv){
  scrolDiv.addEventListener("click", (e) => {
    switch (e.target.id) {
      case "scroll_comment":
        el = document.getElementById("comment_form");
        break;
      case "scroll_share":
        el = document.getElementById("share_form");
        break;
    }
    el.scrollIntoView({
      behavior: "smooth",
      block: "center",
      inline: "center",
    });
  });
}


// preview an image

let img = document.querySelector('.imgPreview')
let imgContainer = document.querySelector(".input_image");
if (imgContainer){
  let currentImg = imgContainer.firstElementChild;
  currentImg.href ? (img.src = currentImg.href) : (img.src = "");
  // currentImg.hidden=true;
  document.getElementById("image-clear_id").classList.add('block-width');
}
