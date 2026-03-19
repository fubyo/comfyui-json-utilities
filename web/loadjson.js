import { app } from '/scripts/app.js';
import { api } from '/scripts/api.js';

function chainCallback(object, property, callback) {
    if (object == undefined) {
        console.error("Tried to add callback to non-existant object");
        return;
    }
    if (property in object && object[property]) {
        const callback_orig = object[property];
        object[property] = function () {
            const r = callback_orig.apply(this, arguments);
            return callback.apply(this, arguments) ?? r;
        };
    } else {
        object[property] = callback;
    }
}

function addUploadWidget(nodeType) {
    chainCallback(nodeType.prototype, "onNodeCreated", function() {
        const node = this;
        const uploadWidget = this.widgets.find((w) => w.name === "upload");
        
        if (!uploadWidget) {
            return;
        }

        const fileInput = document.createElement("input");
        chainCallback(this, "onRemoved", () => {
            fileInput?.remove();
        });

        Object.assign(fileInput, {
            type: "file",
            accept: ".json,application/json",
            style: "display: none",
            onchange: async () => {
                if (fileInput.files.length === 0) {
                    return;
                }

                const file = fileInput.files[0];
                const formData = new FormData();
                formData.append("image", file);

                try {
                    node.progress = { value: 0, text: "Uploading..." };
                    
                    const resp = await fetch(api.apiURL("/upload/image"), {
                        method: "POST",
                        body: formData,
                    });

                    node.progress = undefined;

                    if (resp.status !== 200) {
                        alert(resp.status + " - " + resp.statusText);
                        return;
                    }

                    const data = await resp.json();
                    const filename = data.name;

                    // Update the upload dropdown with the new file
                    if (!uploadWidget.options.values.includes(filename)) {
                        uploadWidget.options.values.push(filename);
                    }
                    uploadWidget.value = filename;

                    // Trigger callback to update the node
                    if (uploadWidget.callback) {
                        uploadWidget.callback(filename);
                    }
                } catch (error) {
                    node.progress = undefined;
                    alert("Upload failed: " + error);
                }
            },
        });

        document.body.appendChild(fileInput);

        const uploadButton = this.addWidget("button", "Choose JSON to upload", null, () => {
            app.canvas.node_widget = null;
            fileInput.click();
        });
        
        uploadButton.options.serialize = false;
    });
}

app.registerExtension({
    name: "comfyui-json-utilities.LoadJSON",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "LoadJSON") {
            addUploadWidget(nodeType);
        }
    }
});
