const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const alertbox = document.getElementById('alert-box')

const handleAlerts = (type, msg) =>{
    alertbox.innerHTML = `
    <div class="alert alert-${type}" role="alert">
        ${msg}
    </div>
    `
}

Dropzone.autoDiscover = false

const myDropzone = new Dropzone("#my-dropzone", {
    url: '/reports/upload/',
    init : function(){
        this.on('sending', function(file, xhr, formData){
            console.log('sending')
            formData.append('csrfmiddlewaretoken', csrf)
        })
        this.on('success', function(file, response){
            console.log(response)
            const ex = response.ex
            if(ex){
                handleAlerts('danger', 'File Already Exists!')
            } else {
                handleAlerts('success', 'Records Saved Successfully')

            }
        })
    },

    maxFiles: 3,
    maxFilesize: 3,
    acceptedFiles: '.csv'
})



