find_friend_input = document.getElementsByName('find_friend_input')[0]
my_friends_ul = document.querySelector('.friends_my')
new_friends_ul = document.querySelector('.friends_search')
requested_friends_ul = document.querySelector('.friends_requested')
alert_div = document.querySelector('.alert_box')
posts = document.querySelector('.posts')

find_friend_input.addEventListener('input', function (evt) {
    if (this.value != '') {
        fetch("friends/search/" + this.value).then(function(response) {
            return response.text()
        }).then(function(text) {
            data = JSON.parse(text)
            if (data['status']) {
                users = data['users']
                users_html = ''
                users.forEach(user => {
                    user_html = `<li class="uk-flex-middle friend_li ` + user["username"] + `">
                            <a href="` + user["username"] + `" class="avatar_a">
                                <img class="uk-border-circle friend_avatar" src="` + user["avatar_url"] + `" alt="Avatar">
                            </a>
                            <a href="` + user["username"] + `" class="names_a">
                                <h3 class="uk-card-title">` + user["first_name"] + ` ` + user["last_name"] + ` <span class="uk-text-meta">` + user["username"] + `</span> </h3>                                        
                            </a>    
                            <a uk-icon="icon: plus" class="icon_for_friend" onclick="friend_add('` + user["username"] + `')"></a>
                        </li>`
                    users_html = users_html + user_html 
                });
                new_friends_ul.innerHTML = users_html
            } else {
                alertfunc(data['error_message'])
            }
        });
    } else {
        new_friends_ul.innerHTML = ''
    }
});

function friend_del(username) {
    if (this.value != '') {
        fetch("friends/delete/" + username).then(function(response) {
            return response.text()
        }).then(function(text) {
            data = JSON.parse(text)
            if (data['status']) {
                document.querySelector("." + username).remove()
            } else {
                alertfunc(data['error_message'])
            }
        });
    } 
}

function friend_add(username) {
    if (this.value != '') {
        fetch("friends/add/" + username).then(function(response) {
            return response.text()
        }).then(function(text) {
            data = JSON.parse(text)
            if (data['status']) {
                document.querySelector("." + username).remove()
            } else {
                alertfunc(data['error_message'])
            }
        });
    } 
}

function friends_get() {
    fetch("friends/get/").then(function(response) {
        return response.text()
    }).then(function(text) {
        data = JSON.parse(text)
        if (data['status']) {
            users = data['users']
            users_html = ''
            users.forEach(user => {
                user_html = `<li class="uk-flex-middle friend_li ` + user["username"] + `">
                        <a href="` + user["username"] + `" class="avatar_a">
                            <img class="uk-border-circle friend_avatar" src="` + user["avatar_url"] + `" alt="Avatar">
                        </a>
                        <a href="` + user["username"] + `" class="names_a">
                            <h3 class="uk-card-title">` + user["first_name"] + ` ` + user["last_name"] + ` <span class="uk-text-meta">` + user["username"] + `</span> </h3>                                        
                        </a>    
                        <a uk-icon="icon: trash" class="icon_for_friend" onclick="friend_del('` + user["username"] + `')"></a>
                    </li>`
                users_html = users_html + user_html 
            });
            my_friends_ul.innerHTML = users_html
        } else {
            alertfunc(data['error_message'])
        }
    });
}

function friends_requested() {
    fetch("friends/requested/").then(function(response) {
        return response.text()
    }).then(function(text) {
        data = JSON.parse(text)
        if (data['status']) {
            users = data['users']
            users_html = ''
            users.forEach(user => {
                user_html = `<li class="uk-flex-middle friend_li ` + user["username"] + `">
                        <a href="` + user["username"] + `" class="avatar_a">
                            <img class="uk-border-circle friend_avatar" src="` + user["avatar_url"] + `" alt="Avatar">
                        </a>
                        <a href="` + user["username"] + `" class="names_a">
                            <h3 class="uk-card-title">` + user["first_name"] + ` ` + user["last_name"] + ` <span class="uk-text-meta">` + user["username"] + `</span> </h3>                                        
                        </a>
                        <a uk-icon="icon: check" class="icon_for_friend" onclick="friend_add('` + user["username"] + `')"></a>    
                        <a uk-icon="icon: close" class="icon_for_friend" onclick="friend_del('` + user["username"] + `')"></a>
                    </li>`
                users_html = users_html + user_html 
            });
            requested_friends_ul.innerHTML = users_html
        } else {
            alertfunc(data['error_message'])
        }
    });
}

function alertfunc(text) {
    alert_div.innerHTML = text
    alert_div.style = 'opacity: 1'
    setTimeout(function opacity() {alert_div.style = 'opacity: 0'}, 3000)
}

document.querySelector('.new_post_form').addEventListener("submit", function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch(this.action, {
        method: this.method,
        body: formData
    }).then(function(response) {
        return response.text()
    }).then(function(text) {
        data = JSON.parse(text)
        if (data['status']) {
            data = data['data']
            new_post = document.createElement('div')
            new_post.setAttribute('class', 'post uk-card uk-card-default')
            new_post.setAttribute('id', 'post_' + data['post_id'])
            pre_new_post = `
            <div class="uk-card-header">
            <div class="uk-grid-small uk-flex-middle uk-grid" uk-grid="">
                <div class="uk-width-auto uk-first-column">
                    <img class="uk-border-circle" width="70" height="70" src="` + data['author']['avatar'] + `" alt="Avatar">
                </div>
                <div class="uk-width-expand">
                    <h3 class="uk-card-title uk-margin-remove-bottom">` + data['author']['first_name'] + ` ` + data['author']['last_name'] + `</h3>
                    <p class="uk-text-meta uk-margin-remove-top">` + data['author']['username'] + `</p>
                </div>
            </div>
        </div>
        <div class="uk-card-body">
            <p class="card_text">` + data['text'] + `</p>
            <div class="post_width_corrector"></div>`
            if (data['img']) {
                pre_new_post = pre_new_post + `<hr>
                <div class="card_imgs">
                <img src="` + data['img'] + `" alt="img" class="card_img"></div>`
            }
            pre_new_post = pre_new_post + `
            <hr>
            <p class="post_created_at">` + data['created_at'] + `</p>
        </div>
        <div class="uk-card-footer post_footer">
            <div class="likes" onclick="post_like('` + data['post_id'] + `')">
                <a uk-icon="icon: heart" class="icon_for_post like_icon"> </a><span class="likes_span"> 0</span>
            </div>
            <div class="post_comments" onclick="post_comm('` + data['post_id'] + `')" uk-toggle="target: #modal-sections-comments_` + data['post_id'] + `">
                <a uk-icon="icon: comments" class="icon_for_post"> </a><span class="post_comments_span"> 0</span>
                <div id="modal-sections-comments_` + data['post_id'] + `" uk-modal>
                    <div class="uk-modal-dialog">
                        <button class="uk-modal-close-default" type="button" uk-close></button>
                        <div class="uk-modal-header">
                            <h2 class="uk-modal-title">Comments</h2>
                        </div>
                        <div class="uk-modal-body">
                            <ul class="uk-list uk-list-divider comments_list" id="comments_list_` + data['post_id'] + `">
                            </ul>
                        </div>
                        <div class="uk-card-footer comments_footer"></div>
                    </div>
                </div>
            </div>
            <div class="warning" onclick="post_warn('` + data['post_id'] + `')" {% endif %}>
                <a uk-icon="icon: warning" class="icon_for_post"> </a><span> Warn</span>
            </div>
        </div>
            `
        new_post.innerHTML = pre_new_post
        posts.appendChild(new_post)
        } else {
            alertfunc(data['error_message'])
        }
    });
    document.querySelector('.new_post_form').reset()
});

function post_like(id) {
    fetch("posts/" + id + "/like/").then(function(response) {
        return response.text()
    }).then(function(text) {
        data = JSON.parse(text)
        if (data['status']) {
            data = data['data']
            post = document.querySelector("#post_" + id)
            post_likes = post.querySelector('.likes')
            post_likes_span = post.querySelector('.likes_span')
            post_comments_span = post.querySelector('.post_comments_span')
            if (data['is_liked']) {
                post_likes.classList.value = 'likes liked'
            } else {
                post_likes.classList.value = 'likes'
            }
            post_likes_span.innerHTML = ' ' + data['likes']
            post_comments_span.innerHTML = ' ' + data['comments_cnt']
        } else {
            alertfunc(data['error_message'])
        }
    });
}

function post_warn(post_id) {
    fetch("posts/" + post_id + "/warn/").then(function(response) {
        return response.text()
    }).then(function(text) {
        data = JSON.parse(text)
        if (data['status']) {
            data = data['data']
            post = document.querySelector("#post_" + post_id)
            post_likes_span = post.querySelector('.likes_span')
            post_comments_span = post.querySelector('.post_comments_span')
            post_warning = post.querySelector('.warning')
            post_warning.classList.value = 'warning warned'
            post_likes_span.innerHTML = ' ' + data['likes']
            post_comments_span.innerHTML = ' ' + data['comments_cnt']
        } else {
            alertfunc(data['error_message'])
        }
    });
}


function post_comm(post_id) {
    new_create_wr = document.querySelector('.comments_create_wrapper').cloneNode(true)
    new_create_form = new_create_wr.querySelector('form')
    new_create_form.setAttribute('action', new_create_form.getAttribute('action').replace('0', String(post_id)))
    new_create_form.removeAttribute('style')
    comments = document.querySelector('#modal-sections-comments_' + post_id + ' > div > .comments_footer')
    comments.innerHTML = new_create_wr.innerHTML
    comment_listener(comments.querySelector('form'))
    fetch("posts/" + post_id + "/comments/").then(function(response) {
        return response.text()
    }).then(function(text) {
        data = JSON.parse(text)
        if (data['status']) {
            data = data['data']
            post = document.querySelector("#post_" + post_id)
            post_comments = document.querySelector('#comments_list_' + post_id)
            post_likes_span = post.querySelector('.likes_span')
            post_comments_span = post.querySelector('.post_comments_span')
            post_likes_span.innerHTML = ' ' + data['likes']
            post_comments_span.innerHTML = ' ' + data['comments_cnt']
            comments_filler(post_id, data['comments'])
        } else {
            alertfunc(data['error_message'])
        }
    });
}

function comment_listener(form) {
    form.addEventListener("submit", function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch(this.action, {
            method: this.method,
            body: formData
        }).then(function(response) {
            return response.text()
        }).then(function(text) {
            data = JSON.parse(text)
            if (data['status']) {
                data = data['data']
                post = document.querySelector("#post_" + data['post_id'])
                post_comments = document.querySelector('#comments_list_' + data['post_id'])
                post_comments_span = post.querySelector('.post_comments_span')
                post_comments_span.innerHTML = ' ' + data['comments_cnt']
                comments_filler(data['post_id'], data['comments'])
            } else {
                alertfunc(data['error_message'])
            }
        });
        form.reset()
    });
}


function comment_like(post_id, comment_id) {
    fetch("posts/" + post_id + "/comments/" + comment_id + "/like/").then(function(response) {
        return response.text()
    }).then(function(text) {
        data = JSON.parse(text)
        if (data['status']) {
            data = data['data']
            comment = document.querySelector('#comment_' + comment_id)
            comment_likes = comment.querySelector('.likes')
            comment_likes_span = comment.querySelector('.likes_span')
            post_comments_span = comment.querySelector('.post_comments_span')
            if (data['is_liked']) {
                comment_likes.classList.value = 'likes liked'
            } else {
                comment_likes.classList.value = 'likes'
            }
            comment_likes_span.innerHTML = ' ' + data['likes']
        } else {
            alertfunc(data['error_message'])
        }
    });
}

function comment_warn(post_id, comment_id) {
    fetch("posts/" + post_id + "/comments/" + comment_id + "/warn/").then(function(response) {
        return response.text()
    }).then(function(text) {
        data = JSON.parse(text)
        if (data['status']) {
            data = data['data']
            comment = document.querySelector('#comment_' + comment_id)
            comment_warning = comment.querySelector('.warning')
            comment_warning.classList.value = 'warning warned'
            comment_likes_span = comment.querySelector('.likes_span')
            comment_likes_span.innerHTML = ' ' + data['likes']
            
        } else {
            alertfunc(data['error_message'])
        }
    });
}


function comments_filler(post_id, comments) {
    post_comments = document.querySelector('#comments_list_' + post_id)
    comments_html = ``
    comments.forEach(comment => {
        comments_html = comments_html + `<li class="comments_li uk-card uk-card-default" id="comment_` + comment['id'] + `">
                        <div class="uk-card-header comment_header">
                            <div class="uk-width-auto uk-first-column comment_header_div">
                                <img class="uk-border-circle" width="60" height="60" src="` + comment['author_avatar_url'] + `" alt="Avatar">
                            </div>
                            <div class="uk-width-expand comment_header_div_mid">
                                <h3 class="uk-card-title uk-margin-remove-bottom">` + comment['author_first_name'] + ` ` + comment['author_last_name'] + `</h3>
                                <p class="uk-text-meta uk-margin-remove-top comment_rem_bottom">` + comment['author_username'] + `</p>
                            </div>
                            <div class="uk-width-expand comment_header_div">
                                <h5 class="uk-text-meta comment_rem_bottom">` + comment['created_at'] + `</h5>
                            </div>
                        </div>
                        <div class="uk-card-body">
                            <p class="comment_text">` + comment['text'] + `</p>`
    if (comment['img_url']) {
        comments_html = comments_html + `<img class="uk-border" width="200" height="200" src="` + comment['img_url'] + `" alt="comment_photo">`
    }
    comments_html = comments_html + `</div>
                        <div class="uk-card-footer comment_footer">
                            <div class="likes" onclick="comment_like(` + comment['post_id'] + `,` + comment['id'] + `)">
                                <a uk-icon="icon: heart" class="icon_for_post like_icon"> </a><span class="likes_span"> ` + comment['likes'] + `</span>
                            </div>
                            <div class="warning" onclick="comment_warn(` + comment['post_id'] + `,` + comment['id'] + `)">
                                <a uk-icon="icon: warning" class="icon_for_post"> </a><span> Warn</span>
                            </div>
                        </div>
                    </li>`
    }); 
    post_comments.innerHTML = comments_html
}


function post_delete(post_id) {
    fetch("posts/" + post_id + "/delete/").then(function(response) {
        return response.text()
    }).then(function(text) {
        data = JSON.parse(text)
        if (data['status']) {
            document.querySelector('#post_' + post_id).remove()
        } else {
            alertfunc(data['error_message'])
        }
    });
}

function post_edit(post_id) {
    post_edit_wr = document.querySelector('.posts_edit_wrapper_form').cloneNode(true)
    post_edit_form = post_edit_wr.querySelector('form')
    post_edit_form.setAttribute('action', post_edit_form.getAttribute('action').replace('0', String(post_id)))
    post_edit_form.removeAttribute('style')
    post_edit_form.querySelector('.post_edit_text > input').value = document.querySelector('#post_' + post_id).querySelector('.card_text').textContent
    img = document.querySelector('#post_' + post_id).querySelector('.card_img')
    if (img.getAttribute('src') != '') {
        post_edit_form.querySelector('.post_edit_img_img').setAttribute('src', img.getAttribute('src'))
    } else {
        post_edit_form.querySelector('.post_edit_img_img').style = 'display: none'
    }
    posts = document.querySelector('#modal-sections-edit_' + post_id).querySelector('.modal_dialog_edit')
    posts.querySelector('.posts_edit_wrapper').innerHTML = post_edit_wr.innerHTML
    posts_edit_listener(posts.querySelector('form'))
}

function posts_edit_listener(form) {
    form.addEventListener("submit", function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch(this.action, {
            method: this.method,
            body: formData
        }).then(function(response) {
            return response.text()
        }).then(function(text) {
            data = JSON.parse(text)
            if (data['status']) {
                data = data['data']
                post = document.querySelector("#post_" + data['post_id'])
                post.querySelector('.card_text').innerHTML = data['text']
                post_imgs = post.querySelector('.post_imgs') 
                post_edit_form = document.querySelector('#modal-sections-edit_' + data['post_id']).querySelector('form')
                if (data['img']) {
                    post_imgs.querySelector('.card_img').setAttribute('src', data['img']) 
                    post_imgs.style = 'display: block'
                    post_edit_form.querySelector('.post_edit_img_img').setAttribute('src', img.getAttribute('src'))
                    post_edit_form.querySelector('.post_edit_img_img').style = 'display: block'
                } else {
                    post_imgs.style = 'display: none'
                    post_edit_form.querySelector('.post_edit_img_img').style = 'display: none'
                }
            } else {
                alertfunc(data['error_message'])
            }
        });
        form.reset()
    });
}
