type Gsheets = { token: string };

export async function main(
  gsheets_auth: Gsheets,
  sheet_id: string,
  dataset: string,
  status: string,
  records_processed: number,
  execution_time_ms: number,
) {
  const token = gsheets_auth.token;
  
  const timestamp = new Date().toISOString();
  
  // Build log entry
  const values = [
    [timestamp, dataset, status, records_processed, execution_time_ms]
  ];
  
  const APPEND_URL = `https://sheets.googleapis.com/v4/spreadsheets/${sheet_id}/values/execution_log:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS`;
  
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
    sheet_tab: "execution_log",
    log_entry: {
      timestamp,
      dataset,
      status,
      records_processed,
      execution_time_ms
    },
    response: result
  };
}