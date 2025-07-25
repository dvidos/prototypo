import React, { useEffect, useState } from "react";

export enum FilterType {
  Text = "text",
  Checkbox = "checkbox",
  Dropdown = "dropdown"
}

export interface FilterAttribute {
  name: string;
  caption: string;
  type: FilterType;
  options?: { value: string; caption: string }[];
}

export type FilterValue = string | boolean | string[] | null;
export type FilterValues = Record<string, FilterValue>;

interface FilterPanelProps {
  attributes: FilterAttribute[];
  values: FilterValues;
  onValuesChanged: (filter_values: FilterValues) => void;
}

const FilterPanel: React.FC<FilterPanelProps> = React.memo(({ attributes, values, onValuesChanged }) => {

  const handleChange = (name: string, value: string | boolean | string[]) => {
    if (value === values[name]) return;
    const newValues = { ...values, [name]: value };
    onValuesChanged(newValues);
  };

  const renderTextInput = (attr: FilterAttribute) => (
    <input
      key={attr.name}
      type="text"
      placeholder={attr.caption}
      value={values[attr.name] as string || ""}
      onChange={(e) => handleChange(attr.name, e.target.value)}
    />
  );

  const renderCheckbox = (attr: FilterAttribute) => (
    <label key={attr.name} style={{ display: "flex", alignItems: "center", gap: 4 }}>
      <input
        type="checkbox"
        checked={Boolean(values[attr.name])}
        onChange={(e) => handleChange(attr.name, e.target.checked)}
      />
      {attr.caption}
    </label>
  );

  const renderDropdown = (attr: FilterAttribute) => (
    <select
      key={attr.name}
      value={values[attr.name] as string || ""}
      onChange={(e) => handleChange(attr.name, e.target.value)}
    >
      <option value="">{attr.caption}</option>
      {attr.options?.map((opt) => (
        <option key={opt.value} value={opt.value}>
          {opt.caption}
        </option>
      ))}
    </select>
  );

  // --- Main render ---
  return (
    <div className="ui-block">
      <strong>Filters</strong>
      <div style={{ display: "flex", gap: "1em", flexWrap: "wrap", marginTop: "0.5em" }}>
        {attributes.map((attr) => {
          switch (attr.type) {
            case FilterType.Text:
              return renderTextInput(attr);
            case FilterType.Checkbox:
              return renderCheckbox(attr);
            case FilterType.Dropdown:
              return renderDropdown(attr);
            default:
              return null;
          }
        })}
      </div>
    </div>
  );
});

export default FilterPanel;
