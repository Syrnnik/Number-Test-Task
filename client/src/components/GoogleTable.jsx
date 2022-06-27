import "../css/App.css";
import { useState, useEffect } from "react";

function GoogleTable() {
    const [Data, SetData] = useState([]);
    const xhr = new XMLHttpRequest();
    xhr.responseType = "json";

    useEffect(() => {
        xhr.open("GET", "http://127.0.0.1:5000/table/");
        // xhr.overrideMimeType("application/json");
        xhr.send();

        xhr.onerror = function () {
            alert("Connection error");
        };

        xhr.onload = function () {
            // alert(`Загружено: ${xhr.status} ${xhr.response}`);
            console.log(xhr.response);
            SetData(xhr.response);
            // console.log(typeof Data);
        };
    });
    // console.log(Data);

    // SetData(
    // fetch("http://127.0.0.1:5000/table/")
    //     .then((response) => {
    //         return response.text();
    //     })
    //     .then((response) => {
    //         SetData(JSON.parse(response));
    //     });
    // );
    // console.log(Data);

    return (
        <div className='google-table'>
            <table>
                <tbody>
                    {/* {console.log(Data)} */}
                    {/* {Data.map(
                        (order) => console.log(order)

                        // <tr key={row}>
                        //     {cols.map((col) => (
                        //         <td key={col} id={row + col}></td>
                        //     ))}
                        // </tr>
                    )} */}
                </tbody>
            </table>
        </div>
    );
}

export default GoogleTable;
