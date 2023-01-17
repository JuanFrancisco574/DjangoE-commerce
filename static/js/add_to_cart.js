var addToCartButtons = document.getElementsByClassName('update-item');
var DeleteFromCartButtons = document.getElementsByClassName('delete-item');

for(i=0; i<addToCartButtons.length; i++){
    var currentButton = addToCartButtons[i];
    currentButton.addEventListener('click', function(){
        var productID = this.dataset.product;
        var action = this.dataset.action;
        console.log('product id: ' + productID + ' action: ' + action);

        updateUserOrder(productID,action);
    });
}

for(i=0; i<DeleteFromCartButtons.length; i++){
    var currentButton = DeleteFromCartButtons[i];
    currentButton.addEventListener('click', function(){
        var productID = this.dataset.product;
        console.log('product id to delete: ' + productID );
        deleteUserOrder(productID);
    });
}

function deleteUserOrder(productID){
    var url = '/deleteitem/';
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productID':productID})
    }).then((response)=>{
        return response.json();
    }).then((data)=>{
        console.log('data: ',data);
        location.reload()
    })
}

function updateUserOrder(productID,action){
    var url = '/updateitem/';
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productID':productID,'action':action})
    }).then((response)=>{
        return response.json();
    }).then((data)=>{
        console.log('data: ',data);
        location.reload()
    })
}