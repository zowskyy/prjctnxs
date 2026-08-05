use nexus_runtime::Runtime;

#[tauri::command]
fn run_frontier(source: String) -> Result<String, String> {
    Runtime::parse_source(&source).map_err(|e| e.to_string())
}

#[tauri::command]
fn engine_status() -> String {
    "Project Nexus v3.0 — runtime connected".into()
}

pub fn launch() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![run_frontier, engine_status])
        .setup(|_app| Ok(()))
        .run(tauri::generate_context!())
        .expect("error while running Project Nexus IDE");
}
