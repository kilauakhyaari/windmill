type Gsheets = { 
  token: string 
};

export async function main(
  gsheets_auth: Gsheets,
  sheet_id: string,
  create_tabs: boolean = true
) {
  const token = gsheets_auth.token;
  
  const requiredTabs = ["weather_data", "user_data", "job_data", "execution_log"];
  
  const GET_URL = `https://sheets.googleapis.com/v4/spreadsheets/${sheet_id}?fields=sheets.properties`;
  
  const response = await fetch(GET_URL, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });
  
  const result = await response.json();
  
  // Check existing tabs
  const existingTabs = result.sheets?.map(sheet => sheet.properties.title) || [];
  const missingTabs = requiredTabs.filter(tab => !existingTabs.includes(tab));
  
  // Create any missing tabs if requested
  if (create_tabs && missingTabs.length > 0) {
    for (const tabName of missingTabs) {
      const ADD_SHEET_URL = `https://sheets.googleapis.com/v4/spreadsheets/${sheet_id}:batchUpdate`;
      
      const addSheetRequest = {
        requests: [
          {
            addSheet: {
              properties: {
                title: tabName,
                gridProperties: {
                  rowCount: 1000,
                  columnCount: 20
                }
              }
            }
          }
        ]
      };
      
      await fetch(ADD_SHEET_URL, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(addSheetRequest),
      });
    }
    
    // Now initialize headers for each tab
    await initializeHeaders(token, sheet_id, missingTabs);
  }
  
  return {
    status: "success",
    sheet_id: sheet_id,
    existing_tabs: existingTabs,
    created_tabs: missingTabs,
    all_tabs_ready: true
  };

  async function initializeHeaders(token, sheetId, tabNames) {
    // Define headers for each tab type
    const headers = {
      "weather_data": ["timestamp", "location", "temperature", "condition", "humidity", "wind_speed"],
      "stock_data": ["timestamp", "symbol", "open", "high", "low", "close", "volume"],
      "covid_data": ["timestamp", "country", "cases", "deaths", "recovered", "active"],
      "execution_log": ["timestamp", "dag_id", "status", "records_processed", "execution_time_ms", "notes"]
    };
    
    // Initialize each tab with headers
    for (const tabName of tabNames) {
      const headerRow = headers[tabName] || ["timestamp", "data"];
      
      const WRITE_URL = `https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values/${tabName}!A1:Z1?valueInputOption=USER_ENTERED`;
      
      await fetch(WRITE_URL, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          values: [headerRow]
        }),
      });
    }
  }
}