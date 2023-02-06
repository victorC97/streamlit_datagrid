import {
  ArrowTable,
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import {Box, Typography} from "@mui/material";
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';


interface State {
}

interface Data {
  rows: object[]
  columns: GridColDef[]
}

const getHeaders = (headers: ArrowTable) => {
  if (headers instanceof ArrowTable) {
    const n = headers.rows
    const res: string[] = []
    for (let i = 1; i < n; i++) {
      // @ts-ignore
      res.push(headers.getCell(i, 1).content.toString())
    }
    return res
  } else {
    return headers
  }
}

const getData = (dataframe: ArrowTable, customHeaders: Array<string>) => {
  const data: Data = {columns: [], rows: []}
  const n = dataframe.rows
  const p = dataframe.columns
  const headers: string[] = []
  data.columns.push({"field": "id", "headerName": "ID", "flex": 1, "editable": false})
  for (let j = 1; j < p; j++) {
    // @ts-ignore
    const field = dataframe.getCell(0, j).content.toString()
    const headerName = customHeaders[j-1]
    if (headerName !== undefined) {
      if (dataframe.getCell(1,j).content instanceof Date) {
        data.columns.push({
          "field": field,
          "headerName": headerName,
          "flex": 1,
          "editable": false,
          "valueFormatter": params => new Date(params?.value).toLocaleString()
        })
      } else {
        data.columns.push({"field": field, "headerName": headerName, "flex": 1, "editable": false})
      }
    }
    headers.push(field)
  }
  for (let i = 1; i < n; i++) {
    const datum: any = {}
    datum["id"] = i
    for (let j = 1; j < p; j++) {
      const content = dataframe.getCell(i, j).content
      if (content instanceof Date) {
        const correctedContent = new Date(content.getTime()*1000000)
        datum[headers[j-1]] = correctedContent
      } else {
        datum[headers[j-1]] = content
      }
    }
    console.log(datum[headers[headers.length - 1]])
    if (datum[headers[headers.length - 1]][0] === 1) {
      data.rows.push(datum)
    }
  }
  return data
}

class StreamlitDatagrid extends StreamlitComponentBase<State> {
  public state = {}
  private dataframe = this.props.args["processed_df"]
  private headers = getHeaders(this.props.args["headers"])

  public render = (): ReactNode => {
    const data: Data = getData(this.dataframe, this.headers)
    return (
        <Box
          sx={{
            height: this.props.args["height"],
            width: "100%",
            paddingLeft: 2
          }}
        >
          <DataGrid
            rows={data.rows}
            columns={data.columns}
            rowHeight={50}
            loading={data.rows.length === 0}
            rowsPerPageOptions={[100]}
            disableSelectionOnClick
          />
        </Box>
    )
  }
}

export default withStreamlitConnection(StreamlitDatagrid)
