const reportBtn = document.getElementById('report-btn');
const reportForm = document.getElementById('report-form');
const img = document.getElementById('img');

// To get Modal Data to Store the values.
// Got IDs by inspecting the modal form.
// Dealing in JS, bcause we used DjangoForms, so cant use the HTML in it.
const reportName = document.getElementById('id_name');
const reportRemarks = document.getElementById('id_remarks');
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;


// For Modal Alert
const alertBox = document.getElementById('alert-box');

const handleAlerts = (type, msg) =>{
    alertBox.innerHTML = `
    <div class="alert alert-${type}" role="alert">
        ${msg}
    </div>
    `
}

// console.log(reportBtn)
// console.log(img)


if(img){
reportBtn.classList.remove('not-visible')
}

// For Adding image into Modal
const modalBody = document.getElementById('modal-body');

reportBtn.addEventListener('click', () => {
    img.setAttribute('class','w-100'); 
    modalBody.prepend(img);

    reportForm.addEventListener('submit', e => {
        // No submit, No refresh
        e.preventDefault();
        
        const fd = new FormData();
        fd.append('name',reportName.value);
        fd.append('image',img.src);
        fd.append('remarks',reportRemarks.value);
        console.log(fd);
        
        $.ajax({
            type: 'POST',
            url: '/reports/save/',
            
            headers:{
                "X-CSRFToken": csrf,
            },
            
            data: fd,

            success: function(response) {
                console.log(response);
                handleAlerts('success', 'Report Created');
                reportForm.reset();
            },
            error:function(error){
                console.log('ERRRRRRRRRR>>>>',error);
                handleAlerts('danger', 'Something went wrong');

            },
            processData: false,
            contentType: false
        });
    })
});