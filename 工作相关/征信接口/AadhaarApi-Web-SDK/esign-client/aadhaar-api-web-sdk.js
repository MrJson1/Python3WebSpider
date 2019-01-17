/**
 * Created by vijay on 08/05/17.
 */
console.log("Gateway Script loaded");
var qmodel = document.getElementById('quaggaModal');
const QUAGGA_BASE_URL = 'https://preprod.aadhaarapi.com';

function isNullUndefinedOrEmpty(paramToCheck) {
    return typeof paramToCheck === 'undefined' || paramToCheck === null || paramToCheck.length === 0;
};

var AadhaarAPIEsignGateway = function(gateway_transaction_id, gatewayOptions, customer_email) {

    if(isNullUndefinedOrEmpty(gateway_transaction_id)) {
        throw new Error('Gateway Transaction Id is mandatory to initiate gateway.');
    }

    if(isNullUndefinedOrEmpty(gatewayOptions.company_display_name)) {
        throw new Error('Company Display Name is mandatory in gateway options.');
    }

    this.gateway_url = QUAGGA_BASE_URL + '/gateway/auth/esign/';
    this.gateway_transaction_id = gateway_transaction_id;
    this.company_display_name = gatewayOptions.company_display_name;
    this.color_bg = gatewayOptions.background_color || null;
    this.color_ft = gatewayOptions.front_text_color || null;
    this.logo_url = gatewayOptions.logo_url || null;
    this.otp_mode = gatewayOptions.otp_allowed || null;
    this.fp_mode = gatewayOptions.fingerprint_allowed || null;
    this.ir_mode = gatewayOptions.iris_allowed || null;
    this.phone_auth = gatewayOptions.phone_auth || null;
    this.draggable_sign = gatewayOptions.draggable_sign || null;
    this.google_sign = gatewayOptions.google_sign || null;
    this.customer_email = customer_email || null;
};

function openAadhaarGateway(gateway) {
    
    //TODO: show loading icon

    let gatewayURI = '' + gateway.gateway_url
        + gateway.gateway_transaction_id + '?';

    if(gateway.company_display_name !== null){
        gatewayURI += '&company_display_name=' +gateway.company_display_name;
    }
    
    if(gateway.color_bg !== null) {
        gatewayURI += '&color_bg=' + gateway.color_bg;
    }

    if(gateway.color_ft !== null) {
        gatewayURI += '&color_ft=' + gateway.color_ft;
    }

    if(gateway.otp_mode !== null) {
        gatewayURI += '&otp_mode=' + gateway.otp_mode;
    }

    if(gateway.fp_mode !== null) {
        gatewayURI += '&fp_mode=' + gateway.fp_mode;
    }

    if(gateway.ir_mode !== null) {
        gatewayURI += '&ir_mode=' + gateway.ir_mode;
    }

    if(gateway.phone_auth === 'y'){
        gatewayURI += '&phone_auth=' + gateway.phone_auth;
    }

    if(gateway.draggable_sign === 'y'){
        gatewayURI += '&draggable_sign=' + gateway.draggable_sign;
    }

    if(gateway.google_sign === 'y'){
        gatewayURI += '&google_sign=' + gateway.google_sign;
    }

    if(gateway.device_selection_allowed !== null) {
        gatewayURI += '&can_select_device=' + gateway.device_selection_allowed;
    }

    if(gateway.customer_email !== null) {
        gatewayURI += '&email=' + gateway.customer_email;
    }

    gatewayURI +='&logo_url=' + gateway.logo_url;

    document.getElementById('quaggaModelContent').innerHTML
        = '<iframe id="quagga-gateway-iframe" height="100%" width="100%" src="'
        + encodeURI(gatewayURI)
        +'"></iframe>';
    // console.log('opening gateway');
    //TODO: show loading icon till the gateway is loaded.
    qmodel.style.display = "block";
}

var CreditScoreGateway=function(gateway_transaction_id,gatewayOptions){
    if(isNullUndefinedOrEmpty(gateway_transaction_id)) {
        throw new Error('Gateway Transaction Id is mandatory to initiate gateway.');
    }

    this.gateway_url = QUAGGA_BASE_URL + '/gateway/auth/creditscore/';
    this.gateway_transaction_id = gateway_transaction_id;
    this.company_display_name = gatewayOptions.company_display_name||'';
    this.color_bg = gatewayOptions.background_color || null;
    this.color_ft = gatewayOptions.front_text_color || null;
    this.logo_url = gatewayOptions.logo_url || null;
    this.full_name=gatewayOptions.full_name||'';
    this.mobile_phone=gatewayOptions.mobile_phone||'';
    this.address_line=gatewayOptions.address_line||'';
    this.state=gatewayOptions.state||'';
    this.postal=gatewayOptions.postal||'';
    this.DOB=gatewayOptions.DOB||'';
    this.customer_panNumber=gatewayOptions.customer_panNumber||'';
    this.otp_mode = gatewayOptions.otp_allowed || null;
    this.fp_mode = gatewayOptions.fingerprint_allowed || null;
    this.ir_mode = gatewayOptions.iris_allowed || null;
    this.phone_auth = gatewayOptions.phone_auth || null;
}

function openAadhaarCSGateway(gateway){
    var gatewayURI = '' + gateway.gateway_url
    + gateway.gateway_transaction_id + '?';


    if(gateway.company_display_name !== null){
        gatewayURI += '&company_display_name=' +gateway.company_display_name;
    }
    
    if(gateway.color_bg !== null) {
        gatewayURI += '&color_bg=' + gateway.color_bg;
    }

    if(gateway.color_ft !== null) {
        gatewayURI += '&color_ft=' + gateway.color_ft;
    }

    gatewayURI +='&logo_url=' + gateway.logo_url;


    if(gateway.full_name!==''){
        gatewayURI+='&full_name='+gateway.full_name;
    }

    if(gateway.address_line!==''){
        gatewayURI+='&address_line='+gateway.address_line;
    }

    if(gateway.state!==''){
        gatewayURI+='&state='+gateway.state;
    }

    if(gateway.postal!==''){
        gatewayURI+='&postal='+gateway.postal;
    }

    if(gateway.DOB!==''){
        gatewayURI+='&DOB='+gateway.DOB;
    }

    if(gateway.customer_panNumber!==''){
        gatewayURI+='&customer_panNumber='+gateway.customer_panNumber;
    }

    document.getElementById('quaggaModelContent').innerHTML
        = '<iframe id="quagga-gateway-iframe" height="100%" width="100%" src="'
        + encodeURI(gatewayURI)
        +'"></iframe>';

    qmodel.style.display = "block";
}

//Listen to close gateway action
console.log('Adding message listener to parent window');
window.addEventListener('message', receiveMessage, false);

function receiveMessage(event) {
    if (event.origin !== QUAGGA_BASE_URL) {
        //console.log"Message is not from Quagga Gateway");
        return;
    }

    //Extracting message from event
    let message = event.data;

    //Do nothing if there is not message
    if (!message) {
        return;
    }

    //handle 'close'
    if (message.action === 'close') {
        qmodel.style.display = 'none';
        document.getElementById('quaggaModelContent').innerHTML = '';
        handleGatewayTermination();
    }

    //handle 'consent-denied'
    if (message.action === 'consent-denied') {
        qmodel.style.display = 'none';
        document.getElementById('quaggaModelContent').innerHTML = '';
        handleEsignConsentDenied();
    }

    //handle 'auth-result'
    if (message.action === 'auth-result') {
        qmodel.style.display = 'none';
        document.getElementById('quaggaModelContent').innerHTML = '';
        if (message.isError) {
            handleAadhaarAUTHFailure(message.payload);
        } else {
            handleAadhaarAUTHSuccess(message.payload);
        }
    }

    //handle 'esign-result'
    if (message.action === 'esign-result') {
        qmodel.style.display = 'none';
        document.getElementById('quaggaModelContent').innerHTML = '';
        if (message.isError) {
            handleAadhaarEsignFailure(message.payload);
        } else {
            handleAadhaarEsignSuccess(message.payload);
        }
    }

    //handle 'otp-error'
    if (message.action === 'otp-error') {
        qmodel.style.display = 'none';
        document.getElementById('quaggaModelContent').innerHTML = '';
        handleAadhaarOTPFailure(message.payload);
    }

    //handle 'gateway-error'
    if (message.action === 'gateway-error') {
        qmodel.style.display = 'none';
        document.getElementById('quaggaModelContent').innerHTML = '';
        handleGatewayError(message.payload);
    }

    //handle 'credit-score-error'
    if (message.action === 'credit-score-result') {
        qmodel.style.display = 'none';
        document.getElementById('quaggaModelContent').innerHTML = '';
        if (message.isError) {
            handleCreditScoreFailure(message.payload);
        } else {
            handleCreditScoreSuccess(message.payload);
        }
    }

}


