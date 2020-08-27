# Home Assistant Custom Component for the Welland Canal Bridges in the Niagara Region of Ontario Canada

<style>.bmc-button img{height: 34px !important;width: 35px !important;margin-bottom: 1px !important;box-shadow: none !important;border: none !important;vertical-align: middle !important;}.bmc-button{padding: 7px 15px 7px 10px !important;line-height: 35px !important;height:51px !important;text-decoration: none !important;display:inline-flex !important;color:#FFFFFF !important;background-color:#FF813F !important;border-radius: 8px !important;border: 1px solid transparent !important;font-size: 24px !important;letter-spacing: 0.6px !important;box-shadow: 0px 1px 2px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 1px 2px 2px rgba(190, 190, 190, 0.5) !important;margin: 0 auto !important;font-family:'Cookie', cursive !important;-webkit-box-sizing: border-box !important;box-sizing: border-box !important;}.bmc-button:hover, .bmc-button:active, .bmc-button:focus {-webkit-box-shadow: 0px 1px 2px 2px rgba(190, 190, 190, 0.5) !important;text-decoration: none !important;box-shadow: 0px 1px 2px 2px rgba(190, 190, 190, 0.5) !important;opacity: 0.85 !important;color:#FFFFFF !important;}</style><link href="https://fonts.googleapis.com/css?family=Cookie" rel="stylesheet"><a class="bmc-button" target="_blank" href="https://www.buymeacoffee.com/djtimca"><img src="https://cdn.buymeacoffee.com/buttons/bmc-new-btn-logo.svg" alt="Buy me a coffee"><span style="margin-left:5px;font-size:24px !important;">Buy me a coffee</span></a>

The status of each of the bridges on the Welland Canal will be reported as new sensors within Home Assistant which can then be used for alerts and status reporting for those who either live near a bridge or who travel across the canal on a regular basis.

## Usage

### Install through HACS:

Add a custom repository in HACS pointed to https://github.com/djtimca/hawellandcanalbridges

The new integration for Welland Canal Bridge Status should appear under your integrations tab.

Click Install and restart Home Assistant.

### Install manually:

Copy the contents found in https://github.com/djtimca/hawellandcanalbridges/custom_components/wellandcanalbridges to your custom_components folder in Home Assistant.

Restart Home Assistant.

### Activate the sensors:

Go to Configuration -> Integrations and click the + to add a new integration.

Search for Welland Canal and you will see the integration available.

Click add, confirm you want to install, and voila... you have the status of all bridges as sensors in your Home Assistant.

Enjoy!
