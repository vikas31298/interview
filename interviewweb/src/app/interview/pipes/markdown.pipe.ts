import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Pipe({
  name: 'markdown',
  standalone:false
})
export class MarkdownPipe implements PipeTransform {

  constructor(private sanitizer: DomSanitizer) {}

  transform(value: string): SafeHtml {
    if (!value) {
      return '';
    }

    // Convert markdown to HTML
    let html = value;

    // Headers
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

    // Bold
    html = html.replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>');
    
    // Italic
    html = html.replace(/\*(.*?)\*/gim, '<em>$1</em>');

    // Links
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/gim, '<a href="$2">$1</a>');

    // Line breaks
    html = html.replace(/\n\n/gim, '</p><p>');
    html = html.replace(/\n/gim, '<br>');

    // Horizontal rules
    html = html.replace(/^---$/gim, '<hr>');

    // Lists - unordered
    html = html.replace(/^\- (.*$)/gim, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>)/gims, '<ul>$1</ul>');

    // Code blocks
    html = html.replace(/`([^`]+)`/gim, '<code>$1</code>');

    // Tables
    html = this.convertTables(html);

    // Wrap in paragraphs if not already in HTML tags
    if (!html.startsWith('<')) {
      html = '<p>' + html + '</p>';
    }

    // Sanitize and return
    return this.sanitizer.bypassSecurityTrustHtml(html);
  }

  private convertTables(html: string): string {
    const lines = html.split('\n');
    let inTable = false;
    let result = '';
    let isHeader = false;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();

      // Check if line is a table row
      if (line.startsWith('|') && line.endsWith('|')) {
        if (!inTable) {
          result += '<table>';
          inTable = true;
          isHeader = true;
        }

        // Check if it's a separator line
        if (line.match(/^\|[\s\-:]+\|$/)) {
          continue;
        }

        // Parse table row
        const cells = line
          .substring(1, line.length - 1)
          .split('|')
          .map(cell => cell.trim());

        if (isHeader) {
          result += '<thead><tr>';
          cells.forEach(cell => {
            result += `<th>${cell}</th>`;
          });
          result += '</tr></thead><tbody>';
          isHeader = false;
        } else {
          result += '<tr>';
          cells.forEach(cell => {
            result += `<td>${cell}</td>`;
          });
          result += '</tr>';
        }
      } else {
        if (inTable) {
          result += '</tbody></table>';
          inTable = false;
        }
        result += line + '\n';
      }
    }

    if (inTable) {
      result += '</tbody></table>';
    }

    return result;
  }
}
