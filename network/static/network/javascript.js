document.addEventListener('DOMContentLoaded', main);

function main(){
    console.log('js file working!')
    userId = document.querySelector('#userid').innerHTML;
    
    editbtn = document.querySelectorAll('#edit-btn');
    editbtn.forEach(editbtn =>{
        editbtn.onclick = ()=>{
            console.log('edit button clicked');
            postCard = editbtn.parentElement.parentElement;
            postId = postCard.children[0].innerHTML;
            console.log('Post ID: ', postId);
            console.log('User ID: ', userId);

            postCard.style.display = 'none';
            editCard = postCard.parentElement.children[1]
            editCard.style.display = 'block';

            submitbtn = editCard.children[0].children[1];
            editform = editCard.children[0];
            editform.onsubmit = () =>{
                console.log("submit button clicked");
                newtext = editCard.children[0].children[0].children[0].value;

                form = new FormData();
                form.append("text", newtext);

                fetch(`/postdata/${postId}`, {
                    method: 'POST',
                    body: form
                })
                postCard.style.display = 'block';
                editCard.style.display = 'none';
                postCard.children[3].innerHTML = newtext;
                console.log("new text: ", editCard.children[0].children[0].children[0].innerHTML);
                console.log("old text: ", postCard.children[3].innerHTML);

                return false;
            }

            //postCard.children[3].innerHTML = editCard.children[0].children[0].children[0].value = newtext;
        }
    })

    likebtn = document.querySelectorAll('.likebtn');
    likebtn.forEach(likebtn =>{
        likebtn.onclick = ()=>{
            console.log('like button clicked')
            postCard = likebtn.parentElement.parentElement;
            postId = postCard.children[0].innerHTML;
            console.log('Post ID: ', postId);
            console.log('User ID: ', userId);
            
            form = new FormData();
            form.append("userid", userId);

            fetch(`/like/${postId}`, {
                method: 'POST',
                body: form
            })
            .then(response => response.json())
            .then(data=> {
                console.log(data);
                console.log(data.likes);
                //likes = postCard.children[4];
                postCard.children[4].innerHTML = `${data.likes} Likes`;
            })

            unlikeDiv = postCard.children[5];
            likeDiv = postCard.children[6];
            likeDiv.style.display = 'none';
            unlikeDiv.style.display = 'block';
        }
    })

    unlikebtn = document.querySelectorAll('.unlikebtn');
    unlikebtn.forEach(unlikebtn =>{
        unlikebtn.onclick = ()=>{
            console.log('unlike button clicked')
            postCard = unlikebtn.parentElement.parentElement;
            postId = postCard.children[0].innerHTML;
            console.log('Post ID: ', postId);
            console.log('User ID: ', userId);

            form = new FormData();
            form.append("userid", userId);

            fetch(`/unlike/${postId}`, {
                method: 'POST',
                body: form
            })
            .then(response => response.json())
            .then(data=> {
                console.log(data);
                console.log(data.likes);
                //likes = postCard.children[4];
                postCard.children[4].innerHTML = `${data.likes} Likes`;
            })

            unlikeDiv = postCard.children[5];
            likeDiv = postCard.children[6];
            likeDiv.style.display = 'block';
            unlikeDiv.style.display = 'none';
        }
    })

}