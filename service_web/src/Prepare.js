import * as React from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import { useGlobal } from 'reactn';

export default function Prepare() {
    const [firstClass, setFirstClass] = useGlobal('firstClass');
    const [secondClass, setSecondClass] = useGlobal('secondClass');
    const [imageCount, setImageCount] = useGlobal('imageCount');
    const onChange = (val) => {
        console.log("val: ", val);
    }

    return (
        <React.Fragment>
            <Typography variant="h6" gutterBottom>
                분류하고자하는 두가지 물체를 입력하세요
            </Typography>
            <Grid container spacing={3}>
                <Grid item xs={12} sm={6}>
                    <TextField
                        required
                        id="firstClass"
                        name="firstClass"
                        label="First Class"
                        fullWidth
                        variant="standard"
                        onChange={e => setFirstClass(e.target.value)}
                    />
                </Grid>
                <Grid item xs={12} sm={6}>
                    <TextField
                        required
                        id="secondClass"
                        name="secondClass"
                        label="Second Class"
                        fullWidth
                        variant="standard"
                        onChange={e => setSecondClass(e.target.value)}
                    />
                </Grid>
                <Grid item xs={12}>
                    <Typography variant="h8" gutterBottom>
                        몇개의 이미지를 사용하시겠습니까?<br /> 많으면 많을수록 시간이 오래걸리지만 좋은 결과를 냅니다 <br /> 최대 100개로 제한합니다.
                    </Typography>
                </Grid>
                <Grid item xs={12}>
                    <TextField
                        required
                        id="count"
                        name="count"
                        label="Image Count"
                        fullWidth
                        variant="standard"
                        type="number"
                        onChange={e => setImageCount(e.target.value)}
                    />
                </Grid>


            </Grid>
        </React.Fragment>
    );
}