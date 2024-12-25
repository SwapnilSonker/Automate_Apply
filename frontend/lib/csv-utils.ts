export function parseEnvToJson(envString: string): Record<string, string> {
    const lines = envString.split('\n').filter(line => line.trim() !== '');
    return lines.reduce((acc, line) => {
      const [key, ...values] = line.split('=');
      if (key && values.length > 0) {
        acc[key.trim()] = values.join('=').trim();
      }
      return acc;
    }, {} as Record<string, string>);
  }
  
  export function convertToCsv(data: Record<string, string>): string {
    const headers = ['Key', 'Value'];
    const rows = Object.entries(data).map(([key, value]) => `"${key}","${value}"`);
    return [headers.join(','), ...rows].join('\n');
  }
  
  export function downloadCsv(csvContent: string, filename: string) {
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }