var tags; 
var input;
var assign_click;
let emailsList = new Array();
let count = 0;




var Handle_assign = (emailsList, id, count, csrf) => function(e){
    while (count < 1) {
        e.preventDefault();
        emailsList=[];
        elements = document.getElementById(`tags_${id}`).children;
        if(elements.length > 0){
            for(var i=0; i<elements.length; i++)
            {
                emailsList.push(elements[i].innerText.slice(0,-1))
            }
        }
        console.log('EML at ASSIGN >>## ',emailsList,id);

        var fd = new FormData();
        for(var i=0; i<emailsList.length; i++)
        {
            fd.append('emails',emailsList[i])
        }

        $.ajax({
            type: 'POST',
            
            url: `/reports/assign_report/${id}`,
            headers:{
                "X-CSRFToken": csrf,
            },
            
            data: fd,
                        
            success: function(response) {
                console.log(response);
            },
            error:function(error){
                console.log('ERRRRRRRRRR>>>>',error);

            },
            processData: false,
            contentType: false
        });

        count++;
        
    }
    
}


function printID(id){
    count = 0
    emailsList = [];
    // Get the tags and input elements from the DOM
    tags = document.getElementById(`tags_${id}`);
    input = document.getElementById(`input-tag_${id}`);
    assign_click = document.getElementById(`button-tag_${id}`);
    const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    console.log(input);

    const tag = document.createElement('li');
    // Get the trimmed value of the input element
    const tagContent = input.value.trim();
    // If the trimmed value is not an empty string
    if (tagContent !== '') {
        // Set the text content of the tag to 
        // the trimmed value
        tag.innerText = tagContent;
        // Add a delete button to the tag
        tag.innerHTML += `<button class="delete-button" onclick="tag_remove(${id})">X</button>`;
        // Append the tag to the tags list
        tags.appendChild(tag);
        // Clear the input element's value
        
    }
    
    // This means, option.value basically.
    input.value = 'select';

    assign_click.addEventListener('click', Handle_assign(emailsList, id, count, csrf));


}


function tag_remove(id){

    tags = document.getElementById(`tags_${id}`);
    const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var get_user_to_remove =''


    if (tags != null)
    {

        // Add an event listener for click on the tags list
        tags.addEventListener('click', function (event) {
    
            // If the clicked element has the class 'delete-button'
            if (event.target.classList.contains('delete-button')) {
                
                console.log(event.target.parentNode);
                console.log(event.target.parentNode.innerText.slice(0,-1));
                get_user_to_remove = event.target.parentNode.innerText.slice(0,-1);
                // Remove the parent element (the tag)
                event.target.parentNode.remove();

                console.log(get_user_to_remove);


                var fdata = new FormData();
                fdata.append('operation','remove_data')
                fdata.append('username',get_user_to_remove)


                $.ajax({
                    type: 'POST',
                    
                    url: `/reports/assign_report/${id}`,
                    headers:{
                        "X-CSRFToken": csrf,
                    },
                    
                    data: fdata,
                                
                    success: function(response) {
                        console.log(response);
                    },
                    error:function(error){
                        console.log('ERRRRRRRRRR>>>>',error);
        
                    },
                    processData: false,
                    contentType: false
                });
        
            }
        });




    
    }
}


// if (tags != null){
//     // Add an event listener for click on the tags list
//     tags.addEventListener('click', function (event) {

//         // If the clicked element has the class 'delete-button'
//         if (event.target.classList.contains('delete-button')) {
        
//             // Remove the parent element (the tag)
//             event.target.parentNode.remove();
//             emailsList.pop()
//         }
//     });

//     }



// elements = document.getElementById(`tags_${id}`).children
// console.log(elements)
// console.log(elements.children);

// if(elements.length > 0){
//     for(var i=0; i<elements.length; i++){
//         emailsList.push(elements[i].innerText.slice(0,-1))
//     }

//     console.log(emailsList);
// }



// console.log('PP',event.target.parentNode.innerText.slice(0,-1));

// element_toremove = event.target.parentNode.innerText.slice(0,-1)


// function arrayRemoveElement(arr, value) {

//     return arr.filter(function (take_eachvalue_fromarray) {
//         // Those != values are pushed into array, = value is not pushed.
//         return take_eachvalue_fromarray != value;
//     });
 
// }
 
// emailsList = arrayRemoveElement(emailsList, element_toremove);

// console.log("REMOV CHCK ::>>>", emailsList);
