import * as React from 'react';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';



export default function Result() {
  const downloadDemo = () => {
    window.open("http://localhost:5000/download_model", "_blank")
  }
  return (
    <React.Fragment>
      <Typography variant="h6" gutterBottom>
        데모 이미지를 확인하고 데모 프로젝트를 다운로드할 수 있습니다.
      </Typography>

      <Grid container spacing={2}>
        <Grid item xs={12} >
          <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
            데모 이미지
          </Typography>

        </Grid>
        <Grid item xs={12} >
          <img src={"http://localhost:5000/result"} width={250} />
        </Grid>
        <Grid item container direction="column" xs={12} >
          <Button variant="contained" onClick={() => downloadDemo()}>다운로드</Button>
        </Grid>
      </Grid>
    </React.Fragment>
  );
}