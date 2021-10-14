function loadAreaAppointment() {
    var appointment_CityId = document.getElementById("appointment_CityId");

    var appointment_AreaId = document.getElementById("appointment_AreaId");

    appointment_AreaId.innerHTML = "";

    var ajax = new XMLHttpRequest();

    ajax.onreadystatechange = function () {

        if (ajax.readyState == 4) {

            var json = JSON.parse(ajax.responseText);

            var option1 = document.createElement("option");

            option1.value = "";
            option1.text = "Select Area";

            appointment_AreaId.options.add(option1);

            for (var i = 0; i < json.length; i++) {

                var option = document.createElement("option");

                option.value = json[i].areaId;
                option.text = json[i].areaName;

                appointment_AreaId.options.add(option)
            }
        }
    };
    ajax.open("get", "/user/ajaxAreaAppointment?appointment_CityId=" + appointment_CityId.value, true);

    ajax.send()
}

function loadBloodBankAppointment() {

    var appointment_AreaId = document.getElementById("appointment_AreaId");

    var appointment_BloodBankId = document.getElementById("appointment_BloodBankId");

    appointment_BloodBankId.innerHTML = "";

    var ajax = new XMLHttpRequest();

    ajax.onreadystatechange = function () {

        if (ajax.readyState == 4) {

            var jsn = JSON.parse(ajax.responseText);

            var option1 = document.createElement("option");

            option1.value = "";
            option1.text = "Select Blood Bank";

            appointment_BloodBankId.options.add(option1);

            for (var i = 0; i < jsn.length; i++) {

                var option = document.createElement("option");

                option.value = jsn[i].bloodBankId;
                option.text = jsn[i].bloodBankName;

                appointment_BloodBankId.options.add(option)
            }
        }
    };
    ajax.open("get", "/user/ajaxBloodBankAppointment?appointment_AreaId=" + appointment_AreaId.value, true);

    ajax.send()
}


function loadTimeSlotAppointment() {

    var appointment_BloodBankId = document.getElementById('appointment_BloodBankId');
    var appointment_TimeSlotId = document.getElementById('appointment_TimeSlotId');

    appointment_TimeSlotId.innerHTML = "";

    var ajax = new XMLHttpRequest();

    ajax.onreadystatechange = function () {

        if (ajax.readyState == 4) {

            console.log(ajax.responseText);

            var jsn = JSON.parse(ajax.responseText);

            var option1 = document.createElement("option");

            option1.value = "";
            option1.text = "Select Time Slot";

            appointment_TimeSlotId.options.add(option1);

            for (var i = 0; i < jsn.length; i++) {
                var option = document.createElement('option');

                option.value = jsn[i].timeSlotId;
                option.text = jsn[i].timeSlot;

                appointment_TimeSlotId.options.add(option)
            }
        }
    };

    ajax.open("get", "/user/ajaxTimeSlotAppointment?appointment_BloodBankId=" + appointment_BloodBankId.value, true);

    ajax.send()
}