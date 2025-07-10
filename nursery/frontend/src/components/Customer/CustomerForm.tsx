import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";


const CustomerForm: React.FC = () => {
  const { id } = useParams();  // From route /customers/:id/edit
  const isEditMode = Boolean(id);
  const navigate = useNavigate();

  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [address, setAddress] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (isEditMode) {
      axios.get(`http://localhost:8000/api/customers/${id}`).then((res) => {
        const c = res.data;
        setFirstName(c.first_name);
        setLastName(c.last_name);
        setEmail(c.email);
        setAddress(c.address);
      });
    }
  }, [id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const payload = { first_name, last_name, email, address };

    try {
      if (isEditMode) {
        await axios.put(`http://localhost:8000/api/customers/${id}`, payload);
        setMessage("Customer updated.");
      } else {
        await axios.post("http://localhost:8000/api/customers", payload);
        setMessage("Customer added.");
      }
      navigate("/customers");  // Redirect to list
    } catch {
      setMessage("Error occurred.");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>{isEditMode ? "Edit" : "Add"} Customer</h2>
      <input type="text" placeholder="First Name" value={first_name} onChange={(e) => setFirstName(e.target.value)} required /><br />
      <input type="text" placeholder="Last Name" value={last_name} onChange={(e) => setLastName(e.target.value)} required /><br />
      <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required /><br />
      <input type="text" placeholder="Address" value={address} onChange={(e) => setAddress(e.target.value)} /><br />
      <button type="submit">Add Customer</button>
      {message && <p>{message}</p>}
    </form>
  );
};

export default CustomerForm;
