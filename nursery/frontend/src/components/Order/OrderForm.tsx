import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axiosInstance from "../../api/axiosInstance";


type OrderLine = {
  sku: string;
  description: string;
  qty: number;
  price: number;
  ext_price: number;
};

type OrderPayload = {
  customer_id: number;
  total: number;
  status: string;
  order_lines: OrderLine[];
};

const OrderForm: React.FC = () => {
  const { id } = useParams(); // `id` is undefined in create mode
  const isEditMode = Boolean(id);
  const navigate = useNavigate();

  const [customerId, setCustomerId] = useState<number | null>(null);
  const [orderLines, setOrderLines] = useState<OrderLine[]>([
    { sku: "", description: "", qty: 1, price: 0, ext_price: 0 },
  ]);
  const [status, setStatus] = useState("draft");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (isEditMode) {
      axiosInstance
        .get(`/orders/${id}`)
        .then((res) => {
          const data = res.data;
          setCustomerId(data.customer_id);
          setOrderLines(data.order_lines);
          setStatus(data.status);
        })
        .catch(() => alert("Failed to load order"))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [id, isEditMode]);

  const handleLineChange = (index: number, field: keyof OrderLine, value: string | number) => {
    const updatedLines = [...orderLines];

    if (field === "qty" || field === "price") {
      const qty = field === "qty" ? Number(value) : updatedLines[index].qty;
      const price = field === "price" ? Number(value) : updatedLines[index].price;
      updatedLines[index].qty = qty;
      updatedLines[index].price = price;
      updatedLines[index].ext_price = qty * price;
    } else {
      updatedLines[index][field] = value as never; // TypeScript workaround if needed
    }

    setOrderLines(updatedLines);
  };

  const addEmptyLine = () => {
    setOrderLines([...orderLines, { sku: "", description: "", qty: 1, price: 0, ext_price: 0 }]);
  };

  const removeLine = (index: number) => {
    const updated = [...orderLines];
    updated.splice(index, 1);
    setOrderLines(updated);
  };

  const calculateTotal = () =>
    orderLines.reduce((sum, l) => sum + l.qty * l.price, 0).toFixed(2);

  const handleSubmit = async () => {
    setSubmitting(true);
    const payload: OrderPayload = {
      customer_id: customerId!,
      total: Number(calculateTotal()),
      status,
      order_lines: orderLines,
    };

    try {
      if (isEditMode) {
        await axiosInstance.put(`/orders/${id}`, payload);
      } else {
        await axiosInstance.post("/orders", payload);
      }
      navigate("/orders");
    } catch {
      alert("Failed to save order");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h2>{isEditMode ? "Edit Order" : "Create Order"}</h2>
      <label>
        Customer ID:{" "}
        <input
          type="number"
          value={customerId ?? ""}
          onChange={(e) => setCustomerId(Number(e.target.value))}
          required
        />
      </label>

      <table border={1} cellPadding={6} style={{ marginTop: "1rem", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>SKU</th>
            <th>Description</th>
            <th>Qty</th>
            <th>Price</th>
            <th>Ext. Price</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {orderLines.map((line, idx) => (
            <tr key={idx}>
              <td>
                <input
                  value={line.sku}
                  onChange={(e) => handleLineChange(idx, "sku", e.target.value)}
                />
              </td>
              <td>
                <input
                  value={line.description}
                  onChange={(e) => handleLineChange(idx, "description", e.target.value)}
                />
              </td>
              <td>
                <input
                  type="number"
                  value={line.qty}
                  min={1}
                  onChange={(e) => handleLineChange(idx, "qty", e.target.value)}
                />
              </td>
              <td>
                <input
                  type="number"
                  step="0.01"
                  value={line.price}
                  onChange={(e) => handleLineChange(idx, "price", e.target.value)}
                />
              </td>
              <td>
                <input
                  type="number"
                  value={orderLines[idx].ext_price}
                  disabled
                  readOnly
                />
              </td>
              <td>{(line.qty * line.price).toFixed(2)}</td>
              <td>
                <button onClick={() => removeLine(idx)} disabled={orderLines.length <= 1}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <button onClick={addEmptyLine} style={{ marginTop: "0.5rem" }}>
        + Add Line
      </button>

      <p>
        <strong>Total:</strong> ${calculateTotal()}
      </p>

      <button onClick={handleSubmit} disabled={submitting || !customerId}>
        {isEditMode ? "Update Order" : "Create Order"}
      </button>
    </div>
  );
};

export default OrderForm;
