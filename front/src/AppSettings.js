class AppSettings {
  static get base_url() {
    return import.meta.env.VITE_BASE_URL
  }
}

export default AppSettings
