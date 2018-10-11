// Block user
function ConfirmBlock(pk){
  swal({
        title: "Blocco Utente",
        text: "Sei sicuro che vuoi disattivare/sospendere questo utente?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Disattiva Utente",
        cancelButtonText: "Chiudi",
        closeOnConfirm: false,
        closeOnCancel: false
    },
    function(isConfirm){
      if (isConfirm){
        request_url = '/banear_user/' + pk
        $.ajax({
              url: request_url,
              success: function(data){
               swal({title: "success", text: 'Utente disabilitato', type: "success", timer: 6000, allowEscapeKey:true});
               location.reload();
              }
            })
            return true;
      }
      else{
        swal({title: "success", text: 'Operazione annullata', type: "success", timer: 3000, allowEscapeKey:true});
        return false;
      }
    })
}

// Active user
function ConfirmDesBlock(pk){
  swal({
        title: "Abilita Utente",
        text: "Sei sicuro che vuoi abilitare questo utente",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Abilita Utente",
        cancelButtonText: "Chiudi",
        closeOnConfirm: false,
        closeOnCancel: false
    },
    function(isConfirm){
      if (isConfirm){
        request_url = '/banear_user/' + pk
        $.ajax({
              url: request_url,
              success: function(data){
               swal({title: "success", text: 'Utente Abilitato', type: "success", timer: 6000, allowEscapeKey:true});
               location.reload();
              }
            })
            return true;
      }
      else{
        swal({title: "success", text: 'Operazione annullata', type: "success", timer: 3000, allowEscapeKey:true});
        return false;
      }
    })
}

// Reset Pass User
function RestarPass(pk){
  swal({
        title: "Reimposta Password",
        text: "Sei sicuro che vuoi reimpostare la password?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Reimpostare",
        cancelButtonText: "Chiudi",
        closeOnConfirm: false,
        closeOnCancel: false
    },
    function(isConfirm){
      if (isConfirm){
        request_url = '/reset_user_password/' + pk
        $.ajax({
              url: request_url,
              success: function(data){
               swal({title: "success", text: 'Password Reimpostata', type: "success", timer: 6000, allowEscapeKey:true});
               location.reload();
              }
            })
            return true;
      }
      else{
        swal({title: "success", text: 'Operazione annullata', type: "success", timer: 3000, allowEscapeKey:true});
        return false;
      }
    })
}

// Delete Contest Solidario
function ContestSolidarioDelete(pk){
  swal({
        title: "Elimina Contest Solidale",
        text: "Sei sicuro che vuoi eliminare questo Contest Solidale?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Elimina",
        cancelButtonText: "Chiudi",
        closeOnConfirm: false,
        closeOnCancel: false
    },
    function(isConfirm){
      if (isConfirm){
        request_url = '/delete_constest_solidario/' + pk
        $.ajax({
              url: request_url,
              success: function(data){
               swal({title: "success", text: 'Elimina', type: "success", timer: 6000, allowEscapeKey:true});
               location.reload();
              }
            })
            return true;
      }
      else{
        swal({title: "success", text: 'Operazione annullata', type: "success", timer: 3000, allowEscapeKey:true});
        return false;
      }
    })
}

// Delete Normall User
function NormalUserDelete(pk){
  swal({
        title: "Elimina Normal - Privati",
        text: "Sei sicuro che vuoi eliminare questo Normal - Privati?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Elimina",
        cancelButtonText: "Chiudi",
        closeOnConfirm: false,
        closeOnCancel: false
    },
    function(isConfirm){
      if (isConfirm){
        request_url = '/delete_normal_user/' + pk
        $.ajax({
              url: request_url,
              success: function(data){
               swal({title: "success", text: 'Elimina', type: "success", timer: 6000, allowEscapeKey:true});
               location.reload();
              }
            })
            return true;
      }
      else{
        swal({title: "success", text: 'Operazione annullata', type: "success", timer: 3000, allowEscapeKey:true});
        return false;
      }
    })
}

// Delete Sponsor
function SponsorUserDelete(pk){
  swal({
        title: "Elimina Sponsor",
        text: "Sei sicuro che vuoi eliminare questo Sponsor?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Elimina",
        cancelButtonText: "Chiudi",
        closeOnConfirm: false,
        closeOnCancel: false
    },
    function(isConfirm){
      if (isConfirm){
        request_url = '/delete_sponsor/' + pk
        $.ajax({
              url: request_url,
              success: function(data){
               swal({title: "success", text: 'Elimina', type: "success", timer: 6000, allowEscapeKey:true});
               location.reload();
              }
            })
            return true;
      }
      else{
        swal({title: "success", text: 'Operazione annullata', type: "success", timer: 3000, allowEscapeKey:true});
        return false;
      }
    })
}


// Delete Terzo Settore
function ThirdUserDelete(pk){
  swal({
        title: "Elimina Terzo Settore",
        text: "Sei sicuro che vuoi eliminare questo Terzo Settore?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Elimina",
        cancelButtonText: "Chiudi",
        closeOnConfirm: false,
        closeOnCancel: false
    },
    function(isConfirm){
      if (isConfirm){
        request_url = '/delete_terzo/' + pk
        $.ajax({
              url: request_url,
              success: function(data){
               swal({title: "success", text: 'Elimina', type: "success", timer: 6000, allowEscapeKey:true});
               location.reload();
              }
            })
            return true;
      }
      else{
        swal({title: "success", text: 'Operazione annullata', type: "success", timer: 3000, allowEscapeKey:true});
        return false;
      }
    })
}


// Delete Terzo Settore
function ShareUserDelete(pk){
  swal({
        title: "Elimina Share Funder",
        text: "Sei sicuro che vuoi eliminare questo Share Funder?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Elimina",
        cancelButtonText: "Chiudi",
        closeOnConfirm: false,
        closeOnCancel: false
    },
    function(isConfirm){
      if (isConfirm){
        request_url = '/delete_share/' + pk
        $.ajax({
              url: request_url,
              success: function(data){
               swal({title: "success", text: 'Elimina', type: "success", timer: 6000, allowEscapeKey:true});
               location.reload();
              }
            })
            return true;
      }
      else{
        swal({title: "success", text: 'Operazione annullata', type: "success", timer: 3000, allowEscapeKey:true});
        return false;
      }
    })
}

// Delete Competition
function CompetitionDelete(pk){
  swal({
        title: "Delete competition",
        text: "¿You are sure you want to delete the competition?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Delete",
        cancelButtonText: "Cancel",
        closeOnConfirm: false,
        closeOnCancel: false
    },
    function(isConfirm){
      if (isConfirm){
        request_url = '/delete_competition/' + pk
        $.ajax({
              url: request_url,
              success: function(data){
               swal({title: "success", text: 'Delete', type: "success", timer: 6000, allowEscapeKey:true});
               location.reload();
              }
            })
            return true;
      }
      else{
        swal({title: "success", text: 'Operation cancelled', type: "success", timer: 3000, allowEscapeKey:true});
        return false;
      }
    })
}

// Delete Competition
function downloadUserInfo(pk){
  swal({
        title: "Download user info in excel",
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Download",
        closeOnConfirm: false,
    },
    function(){
        request_url = '/api-validate_point_competition/' + pk
        $.ajax({
              url: request_url,
              success: function(data){
                if(data.validate){
                  request_url = '/api/excel_users_info/' + pk
                  var win = window.open(request_url, '_blank');
                  win.focus();
                  swal({
                    icon: "success",
                    title: "Success"
                  });
                }
                else{
                  swal({
                    icon: "warning",
                    title: "This competition no have user info"
                  });
                }
              }
            })
            return true;
      }
    )
}


function openInNewTab(url) {
  
}