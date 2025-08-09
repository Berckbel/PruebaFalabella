import { useCallback, useEffect, useState } from 'react'
import './App.css'

function App() {
  const [documentTypes, setDocumentTypes] = useState([])
  const [bills, setBills] = useState([])
  const [searchParams, setSearchParams] = useState({ docType: '', docNumber: '' })

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/v1/client/document-types/')
      .then(response => response.json())
      .then(data => {
        setDocumentTypes(data)
      })
      .catch(error => {
        console.error('Error fetching document types:', error)
      })
  }, [])

  const getClientBills = useCallback(({ docType, docNumber }) => {
    fetch(`http://127.0.0.1:8000/api/v1/sale/bills/?doc_type=${docType}&doc_number=${docNumber}`)
      .then(response => response.json())
      .then(data => {
        setBills(data)
      })
      .catch(error => {
        console.error('Error fetching bills:', error)
      })
  }, [])

  const handleSubmit = (event) => {
    event.preventDefault()
    const formData = new FormData(event.target);
    const { docType, docNumber } = Object.fromEntries(formData.entries());

    setSearchParams({ docType, docNumber });

    getClientBills({ docType, docNumber });
  }

  return (
    <>
      <div>

        <form onSubmit={handleSubmit}>
          <select name="docType" id="docType">
            <option value="">Select Document Type</option>
            {documentTypes.map((type) => (
              <option key={type.id} value={type.id}>
                {type.name}
              </option>
            ))}
          </select>
          <label>
            Document Number:
            <input type="text" name="docNumber" id="docNumber" />
          </label>
          <button>Buscar</button>
        </form>

        <div>
          {
            (bills.length > 0) &&
            <a
              href={`http://127.0.0.1:8000/api/v1/sale/export-data/${searchParams.docType}/${searchParams.docNumber}/`}
              target='_blank'
            >
              Export Data
            </a>
          }
        </div>

        <div className='bills'>
          {bills.map((bill) => (
            <div key={bill.id} className='bill'>
              <h3>Bill ID: {bill.id}</h3>
              <p>Client: {bill.client.first_name} {bill.client.last_name}</p>
              {bill.sales.map(sale => (
                <table border={2} key={sale.id}>
                  <thead>
                    <tr>
                      <th>SKU</th>
                      <th>Quantity</th>
                      <th>Price</th>
                      <th>Total</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{sale.product.sku}</td>
                      <td>{sale.product_quantity}</td>
                      <td>{sale.product_price}</td>
                      <td>{sale.sale_total}</td>
                    </tr>
                  </tbody>
                </table>
              ))}
              <p>Total Bill: {bill.billing_total}</p>
              <strong>Billing date: {bill.billing_date}</strong>
            </div>
          ))}
        </div>
      </div>
    </>
  )
}

export default App
