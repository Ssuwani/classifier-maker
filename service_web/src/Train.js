import * as React from 'react';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { useGlobal } from 'reactn';
import axios from 'axios';

export default function Train() {
    const [firstClass, setFirstClass] = useGlobal('firstClass');
    const [secondClass, setSecondClass] = useGlobal('secondClass');
    const [imageCount, setImageCount] = useGlobal('imageCount');

    const onTrainButtonClicked = async () => {
        console.log(`Train Button Cliked `)
        console.log(`classes: ${firstClass},${secondClass}`)
        console.log(`imageCount: ${imageCount}`)
        const response = await axios({
            method: 'post',
            url: 'http://localhost:5000/run',
            data: {
                classes: `${firstClass},${secondClass}`,
                imageCount: imageCount
            }
        });
        console.log(response)
        console.log(response.status)
        // if (response.status == 200) {
        //     setResultImageUrl(`http://localhost:5000/result/${userId}`)
        // }
    }

    return (
        <React.Fragment>
            <Typography variant="h6" gutterBottom>
                버튼을 클릭하면 학습이 시작됩니다. <br /> 이미지 50개 기준 약 5분이 소요됩니다.
            </Typography>
            <Grid container spacing={3}>

                <Grid
                    container
                    item xs={12}
                    direction="column"
                    alignItems="center"
                    justifyContent="center"
                >
                    <Button variant="contained" onClick={() => onTrainButtonClicked()}>학습하기</Button>
                </Grid>
            </Grid>
        </React.Fragment>
    );
}