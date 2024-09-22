import {
  JupyterFrontEnd, JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  INotebookTracker, NotebookPanel
} from '@jupyterlab/notebook';

import {
  CodeCell
} from '@jupyterlab/cells';

import {
  KernelMessage
} from '@jupyterlab/services';

import {
  ToolbarButton
} from '@jupyterlab/apputils';

/**
 * Initialization data for the extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'your-extension-name',
  autoStart: true,
  requires: [INotebookTracker],
  activate: (app: JupyterFrontEnd, tracker: INotebookTracker) => {

    const command = 'your-extension:check-code';
    app.commands.addCommand(command, {
      label: 'Check HTML, CSS, and JavaScript',
      execute: async () => {
        const current = tracker.currentWidget;
        if (current) {
          const notebook = current as NotebookPanel;
          const activeCell = notebook.content.activeCell;

          if (activeCell && activeCell.model.type === 'code') {
            const codeCellModel = activeCell.model as any;
            const code = codeCellModel.sharedModel.getSource();

            const fileType = determineFileType(code);

            if (fileType) {
              const kernel = current.sessionContext.session?.kernel;
              if (kernel) {
                const future = kernel.requestExecute({
                  code: `exec(open("C:/Users/musma/Desktop/Extension/src/code_linter.py").read())

code = \"\"\"${code}\"\"\"  # Safely handle multiline strings for code
file_type = "${fileType}"

result = lint_code(code, file_type)
print(format_lint_results(result, file_type))
`.trim()
                });

                future.onIOPub = (msg: KernelMessage.IIOPubMessage) => {
                  if (msg.header.msg_type === 'stream') {
                    const content = msg.content as KernelMessage.IStreamMsg['content'];
                    if (content.name === 'stdout') {
                      const result = content.text;

                      if (activeCell instanceof CodeCell) {
                        const codeCell = activeCell as CodeCell;
                        const model = codeCell.model;
                        const outputs = model.outputs;

                        if (outputs) {
                          const newOutput = {
                            output_type: 'execute_result',
                            data: { 'text/html': `<pre>${result}</pre>` },
                            metadata: {},
                            execution_count: null
                          };

                          // Prepend the new output at the top
                          const allOutputs = outputs.toJSON();
                          outputs.clear(); // Clear existing outputs
                          outputs.add(newOutput); // Add the new result
                          allOutputs.forEach(output => outputs.add(output)); // Re-add the previous outputs
                        }
                      }
                    }
                  } else if (msg.header.msg_type === 'error') {
                    console.error('Kernel error:', msg.content);
                    if (activeCell instanceof CodeCell) {
                      const codeCell = activeCell as CodeCell;
                      const model = codeCell.model;
                      const outputs = model.outputs;

                      if (outputs) {
                        const errorContent = msg.content as KernelMessage.IErrorMsg['content'];
                        outputs.add({
                          output_type: 'error',
                          evalue: errorContent.evalue,
                          traceback: errorContent.traceback
                        });
                      }
                    }
                  }
                };

                future.done.then(() => {
                  console.log('Kernel execution finished');
                }).catch(console.error);
              }
            }
          }
        }
      }
    });

    // Add a toolbar button for the command
    tracker.widgetAdded.connect((_, panel) => {
      const button = new ToolbarButton({
        label: 'Check Code',
        onClick: () => {
          app.commands.execute(command);
        },
        tooltip: 'Check HTML, CSS, and JavaScript',
        className: 'jp-ToolbarButtonComponent', // Add a class for styling
      
      });

      panel.toolbar.insertItem(10, 'checkCode', button);
    });
  }
};

function determineFileType(code: string): string | null {
  if (code.includes('<html') || code.includes('<!DOCTYPE html>')) {
    return 'html';
  } else if (code.includes('function') || code.includes('var') || code.includes('let') || code.includes('const')) {
    return 'js';
  } else if (code.includes('body') || code.includes('css')) {
    return 'css';
  }
  return null;
}

export default plugin;
