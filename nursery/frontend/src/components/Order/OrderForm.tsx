import React, { useState, useEffect } from "react";
import axios from "axios";


const OrderForm: React.FC = () => {
  const [customerId, setCustomerId] = useState<number | "">("");
  const [item, setItem] = useState("");
  const [quantity, setQuantity] = useState<number | "">("");
  const [status, setStatus] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (customerId === "" || quantity === "") {
      setMessage("Customer ID and quantity are required");
      return;
    }
    try {
      await axios.post("http://localhost:8000/api/orders", {
        customerId,
        item,
        quantity,
        status,
      });
      setMessage("Order added successfully");
      setCustomerId("");
      setItem("");
      setQuantity("");
      setStatus("");
    } catch {
      setMessage("Failed to add order");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Add Order</h2>
      <input
        type="number"
        placeholder="Customer ID"
        value={customerId}
        onChange={(e) => setCustomerId(Number(e.target.value))}
        required
      /><br />
      <input
        type="text"
        placeholder="Item"
        value={item}
        onChange={(e) => setItem(e.target.value)}
      /><br />
      <input
        type="number"
        placeholder="Quantity"
        value={quantity}
        onChange={(e) => setQuantity(Number(e.target.value))}
        required
      /><br />
      <input
        type="text"
        placeholder="Status"
        value={status}
        onChange={(e) => setStatus(e.target.value)}
      /><br />
      <button type="submit">Add Order</button>
      {message && <p>{message}</p>}
    </form>
  );
};

export default OrderForm;
