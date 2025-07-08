entity Customer {
  attributes {
    LegalName
    PreferredName
    Email
    Address
  }
  actions {
    Register
    Subscribe {
        description: "Subscribe to our newsletter"
        command {
            Email: String
        }
        response {
            success: Boolean
            message: String
        }
    }
    Unsubscribe
  }
}
