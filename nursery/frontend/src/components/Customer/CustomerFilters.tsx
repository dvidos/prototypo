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
    <div className="ui-block">
      <strong>Filters</strong>

      <input
        type="text"
        placeholder="First name contains..."
        value={filters.firstName}
        onChange={(e) => handleChange("firstName", e.target.value)}
        style={{ marginLeft: "1em"}}
      />

      <input
        type="text"
        placeholder="Email contains..."
        value={filters.email}
        onChange={(e) => handleChange("email", e.target.value)}
        style={{ marginLeft: "1em"}}
      />

      <input
        type="text"
        placeholder="Address contains..."
        value={filters.address}
        style={{ marginLeft: "1em"}}
        onChange={(e) => handleChange("address", e.target.value)}
      />
    </div>
  );
});

export default CustomerFilters;
