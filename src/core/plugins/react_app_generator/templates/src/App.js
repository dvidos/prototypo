import React, { useState } from "react";

const TABS = [
  { key: "customers", label: "Customers" },
  // Add more entities here later
];

function App() {
  const [activeTab, setActiveTab] = useState("customers");

  return (
    <div>
      <h1>Entity Manager</h1>
      {% raw %}
      <div style={{ display: "flex", gap: 8 }}>
        {TABS.map(tab => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            style={{ fontWeight: activeTab === tab.key ? "bold" : "normal" }}
          >
            {tab.label}
          </button>
        ))}
      </div>
      {% endraw %}
      <hr />
      {activeTab === "customers" && <Customers />}
      {/* Add more entities here */}
    </div>
  );
}

function Customers() {
  const [customers, setCustomers] = useState([]);
  const [selected, setSelected] = useState(null);
  const [form, setForm] = useState({ fullname: "", address: "" });

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  function handleSubmit(e) {
    e.preventDefault();
    if (selected === null) {
      setCustomers([...customers, { ...form, id: Date.now() }]);
    } else {
      setCustomers(customers.map(c => c.id === selected ? { ...form, id: selected } : c));
      setSelected(null);
    }
    setForm({ fullname: "", address: "" });
  }

  function handleEdit(id) {
    const cust = customers.find(c => c.id === id);
    setForm({ fullname: cust.fullname, address: cust.address });
    setSelected(id);
  }

  function handleDelete(id) {
    setCustomers(customers.filter(c => c.id !== id));
    if (selected === id) {
      setSelected(null);
      setForm({ fullname: "", address: "" });
    }
  }

  function handleView(id) {
    const cust = customers.find(c => c.id === id);
    alert(`Fullname: ${cust.fullname}\nAddress: ${cust.address}`);
  }

  return (
    <div>
      <h2>Customers</h2>
      <form onSubmit={handleSubmit}>
        <input
          name="fullname"
          placeholder="Fullname"
          value={form.fullname}
          onChange={handleChange}
          required
        />
        <input
          name="address"
          placeholder="Address"
          value={form.address}
          onChange={handleChange}
          required
        />
        <button type="submit">{selected === null ? "Add" : "Update"}</button>
        {selected !== null && (
          <button type="button" onClick={() => { setSelected(null); setForm({ fullname: "", address: "" }); }}>
            Cancel
          </button>
        )}
      </form>
      <ul>
        {customers.map(c => (
          <li key={c.id}>
            {c.fullname} ({c.address})
            <button onClick={() => handleView(c.id)}>View</button>
            <button onClick={() => handleEdit(c.id)}>Edit</button>
            <button onClick={() => handleDelete(c.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
