type Gsheets = { token: string };

export async function main(
  gsheets_auth: Gsheets,
  sheet_id: string,
  sheet_tab: string,
  records: any[],
  include_headers: boolean = false
) {
  const token = gsheets_auth.token;
  
  if (!records || records.length === 0) {
    return {
      status: "warning",
      message: "No records to load",
      sheet_id: sheet_id,
      sheet_tab: sheet_tab
    };
  }
  
  // Extract headers from first record
  const headers = Object.keys(records[0]);
  
  // Build values array (2D array for sheets)
  const values: any[][] = [];
  
  // Add headers row if requested
  if (include_headers) {
    values.push(headers);
  }
  
  // Add data rows
  records.forEach(record => {
    const row = headers.map(header => {
      const value = record[header];
      return value === null || value === undefined ? "" : value;
    });
    values.push(row);
  });
  
  const APPEND_URL = `https://sheets.googleapis.com/v4/spreadsheets/${sheet_id}/values/${sheet_tab}:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS&includeValuesInResponse=true`;
  
  const response = await fetch(APPEND_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ values }),
  });
  
  const result = await response.json();
  
  return {
    status: "success",
    sheet_id: sheet_id,
    sheet_tab: sheet_tab,
    rows_written: values.length,
    response: result
  };
}