function buttonclickhandler() {

    const xhr = new XMLHttpRequest();
    let query = document.getElementById("q").value;

    let base_url = "http://127.0.0.1:8000"

    xhr.open("GET", base_url + "/api/search/?q=" + query, true);

    xhr.onload = function() {

            if (this.status === 200) {
                obj = JSON.parse(this.responseText);
                let list = document.getElementById("my_container");

                list.innerHTML = `
            ${ obj.map(function(post){
                return `
                <article class="media content-section">
                <img class="rounded-circle article-img" src="${ post.owner.image }">
                <div class="media-body">
                    <div class="article-metadata">
                    <a class="mr-2" href="${ post.owner.profile_url }">${ post.owner.username }</a>
                    <small class="text-muted">${ post.date_posted }</small>
                    </div>
                    <h1><a class="article-title" href="${ post.post_url }">${post.title}</a></h1>
                    <div class='row'>
                    <div class="col-md-8">
                        <div class='post-content'>
                            <p class="text-justify" class="article-content">${post.description}</p>   
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class='post-img'>
                        <img class="img-fluid" src="${ post.thumbnail_image }">
                        </div>
                    </div>
                    </div>
                <div class="btn-toolbar py-3">
                    <a  class="btn btn-success btn-md px-5 mr-3" href="${ post.uploaded_file }">Download</a>
                    </div>
                </div>
                </article>
                `
            })}`;
        }
    }
    xhr.send();
}