# Home Assistant Custom Component for the Welland Canal Bridges in the Niagara Region of Ontario Canada

<a target="_blank" href="https://www.buymeacoffee.com/djtimca"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy me a coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;"></a>[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

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
