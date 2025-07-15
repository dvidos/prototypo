import React, { useEffect, useState } from "react";

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
  const [localFilters, setLocalFilters] = useState(filters);

  useEffect(() => {
    setLocalFilters(filters);
  }, [filters]);

  const DEBOUNCE_DELAY_MSECS = 300;

  useEffect(() => {
    const timeout = setTimeout(() => { onChange(localFilters); }, DEBOUNCE_DELAY_MSECS);
    return () => clearTimeout(timeout);
  }, [localFilters, onChange]);

  const handleChange = (field: keyof CustomerFilterValues, value: string) => {
    setLocalFilters((prev) => ({
      ...filters,
      [field]: value,
    }));
  };

  return (
    <div className="ui-block">
      <strong>Filters</strong>

      <input
        type="text"
        placeholder="First name contains..."
        value={localFilters.firstName}
        onChange={(e) => handleChange("firstName", e.target.value)}
        style={{ marginLeft: "1em"}}
      />

      <input
        type="text"
        placeholder="Email contains..."
        value={localFilters.email}
        onChange={(e) => handleChange("email", e.target.value)}
        style={{ marginLeft: "1em"}}
      />

      <input
        type="text"
        placeholder="Address contains..."
        value={localFilters.address}
        style={{ marginLeft: "1em"}}
        onChange={(e) => handleChange("address", e.target.value)}
      />
    </div>
  );
});

export default CustomerFilters;
