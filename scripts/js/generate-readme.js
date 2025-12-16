import { expandSnippets } from './snippetExpander.js';

const args = process.argv.slice(2);

let addLineNumbers = true;
if (args.includes('--no-lines')) {
  addLineNumbers = false;
  args.splice(args.indexOf('--no-lines'), 1);
}

if (args.length === 0) {
  expandSnippets('.', null, addLineNumbers);
} else if (args.length === 1) {
  expandSnippets(args[0], null, addLineNumbers);
} else {
  expandSnippets(args[0], args[1], addLineNumbers);
}
