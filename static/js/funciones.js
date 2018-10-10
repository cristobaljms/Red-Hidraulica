$(document).ready(function () {
    $('#beneficiarios_tabla').DataTable();
});

// Active user
function ConfirmDesBlock(pk){
    swal({
        title: "Deshabilitar Beneficiario",
        text: "¿Seguro que desea borrar este beneficiario?",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((willDelete) => {
        if (willDelete) {
        request_url = '/beneficiarios/eliminar/' + pk
          $.ajax({
                url: request_url,
                success: function(data){
                    swal({title: "OK", text: 'Beneficiario deshabilitado', type: "success", timer: 6000, allowEscapeKey:true});
                    location.reload();
                }
              })
              return true;
        } else {
            swal("Operacion cancelada");
        }
    });
  }