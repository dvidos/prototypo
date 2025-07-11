import React from "react";

export interface CustomerFilterValues {
  firstName: string;
  email: string;
  address: string;
}

interface CustomerFiltersProps {
  filters: CustomerFilterValues;
  onChange: (filters: CustomerFilterValues) => void;
}

const CustomerFilters: React.FC<CustomerFiltersProps> = React.memo(({ filters, onChange }) => {
  const handleChange = (field: keyof CustomerFilterValues, value: string) => {
    onChange({
      ...filters,
      [field]: value,
    });
  };

  return (
    <div style={{ marginBottom: 12, padding: 8, border: "1px solid #ccc", borderRadius: 4 }}>
      <strong>Filters</strong>
      <br />
      <input
        type="text"
        placeholder="First name contains..."
        value={filters.firstName}
        onChange={(e) => handleChange("firstName", e.target.value)}
        style={{ marginBottom: 8, display: "block" }}
      />
      <input
        type="text"
        placeholder="Email contains..."
        value={filters.email}
        onChange={(e) => handleChange("email", e.target.value)}
        style={{ marginBottom: 8, display: "block" }}
      />
      <input
        type="text"
        placeholder="Address contains..."
        value={filters.address}
        onChange={(e) => handleChange("address", e.target.value)}
      />
    </div>
  );
});

export default CustomerFilters;
