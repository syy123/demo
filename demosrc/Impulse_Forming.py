import random;
import numpy;
import pylab;

class ImpulseForming():
    def __init__(self, PulseNumber, PilotNumber, pixelNumber, filter_left_x, filter_right_x, alpha, CarrierFc):
        self.PulseNumber = PulseNumber;
        self.PulseNumberXRight = PulseNumber / 2;
        self.PulseNumberXLeft = -1 * self.PulseNumberXRight;
        self.pixelNumber = pixelNumber;
        self.filter_left_x = filter_left_x;
        self.filter_right_x = filter_right_x;
        self.alpha = alpha;
        self.CarrierFc = CarrierFc;
        self.PilotNumber = PilotNumber;
        
    def CalculateAllPixel(self):
        return (self.filter_right_x - self.filter_left_x) * self.pixelNumber;      
    
    def GetRaisedCosineArray(self):
        self.FilterArrayX = numpy.linspace(self.filter_left_x, self.filter_right_x, self.CalculateAllPixel());
        self.RaisedCosineYArray = self.Raised_cosine_time(self.alpha, self.FilterArrayX);
        
    def Raised_cosine_time(self, a, x):
        return (numpy.sin(numpy.pi * x) / (numpy.pi * x)) * (numpy.cos(a * numpy.pi * x) / (1 - 4 * a **2 * x ** 2));

    def CreateRandomNumber(self):
        binaryData = [1, 0, 1, 0, 1, 1, 0, 1];
        self.PilotLength = len(binaryData);
        for i in range(self.PulseNumber):
            binaryData.append(random.randint(0, 1));
        return binaryData;
        
    def CreateRectArray(self, randomNumber):
        Array = [];
        for i in range(len(randomNumber)):
            if (randomNumber[i] == 0):
                for j in range(1):
                    Array.append(-1);
                for j in range(1, self.pixelNumber):
                    Array.append(0);
            else:
                for j in range(1):
                    Array.append(1);
                for j in range(1, self.pixelNumber):
                    Array.append(0);
        return Array;

    def CreateQPSKPilotData(self):
        PilotData = [];
        for i in range(self.PilotNumber * 2):
            PilotData.append(random.randint(0, 1));
        return PilotData;
    
    def GetPilotRealImageArray(self):
        PilotBinaryData = self.CreateQPSKPilotData();
        PilotRealArray, PilotImageArray = self.QPSKRealImageArray(PilotBinaryData);
        
        PilotXArray = numpy.linspace(-1 * self.PilotNumber / 2,
                                          self.PilotNumber / 2,
                                          len(PilotRealArray));
        
        return PilotXArray, PilotBinaryData, PilotRealArray, PilotImageArray;
        
    def CreateQPSKUserData(self):
        UserData = [];
        for i in range(self.PulseNumber * 2):
            UserData.append(random.randint(0, 1));
        return UserData;

    def GetUserRealImageArray(self):
        UserBinaryData = self.CreateQPSKUserData();
        UserRealArray, UserImageArray = self.QPSKRealImageArray(UserBinaryData);
        
        UserXArray = numpy.linspace(self.PulseNumberXLeft, 
                                          self.PulseNumberXRight, 
                                          len(UserRealArray));
        
        return UserXArray, UserBinaryData, UserRealArray, UserImageArray;

    def CreateQPSKUserAndPilotData(self):
        PilotData = self.CreateQPSKPilotData();
        UserData = self.CreateQPSKUserData();
        PilotAndUserData = PilotData + UserData;
        return PilotAndUserData;
        
    def GetPilotAndUserRealImageArray(self):
        self.GetPilotRealImageArray();
        self.GetUserRealImageArray();
        self.PilotAndUserRealArray = self.PilotRealArray + self.UserRealArray;
        self.PilotAndUserImageArray = self.PilotImageArray + self.UserImageArray;
        
    def ConvolvePilotRealImageData(self, PilotReal, PilotImage, RaisedCosineArray):
        self.ConPilotRealYArray = [];
        self.ConPilotImageYArray = [];
        
        ConPilotRealYArray = numpy.convolve(PilotReal, RaisedCosineArray);
        ConPilotRealXArray = numpy.linspace(self.filter_left_x - self.PilotNumber / 2, 
                             self.filter_right_x + self.PilotNumber / 2, 
                             len(ConPilotRealYArray));
                                                  
        ConPilotImageYArray = numpy.convolve(PilotImage, RaisedCosineArray);
        ConPilotImageXArray = numpy.linspace(self.filter_left_x - self.PilotNumber / 2, 
                             self.filter_right_x + self.PilotNumber / 2, 
                             len(ConPilotImageYArray));
                             
        return ConPilotRealXArray, ConPilotRealYArray, ConPilotImageXArray, ConPilotImageYArray;
    
    def ConvolveUserRealImageData(self, UserReal, UserImage, RaisedCosineArray):
        self.ConUserRealYArray = [];
        self.ConUserImageYArray = [];
        
        ConUserRealYArray = numpy.convolve(UserReal, RaisedCosineArray);
        ConUserRealXArray = numpy.linspace(self.filter_left_x + self.PulseNumberXLeft, 
                             self.filter_right_x + self.PulseNumberXRight, 
                             len(ConUserRealYArray));
                                                  
        ConUserImageYArray = numpy.convolve(UserImage, RaisedCosineArray);
        ConUserImageXArray = numpy.linspace(self.filter_left_x + self.PulseNumberXLeft, 
                             self.filter_right_x + self.PulseNumberXRight, 
                             len(ConUserImageYArray));
                             
        return ConUserRealXArray, ConUserRealYArray, ConUserImageXArray, ConUserImageYArray;
                             
    def ModulatePilotRealImageData(self, ConPilotReal, ConPilotImage):
        PilotModulateYData = [];
        
        PilotModulateXData = numpy.arange(-1 * self.PilotNumber / 2, 
                                          self.PilotNumber / 2, 
                                          1.0 / self.pixelNumber);
                             
        PilotRealY = ConPilotReal[self.filter_right_x * self.pixelNumber : (self.PilotNumber +  self.filter_right_x) * self.pixelNumber];
        PilotImageY = ConPilotImage[self.filter_right_x * self.pixelNumber : (self.PilotNumber +  self.filter_right_x) * self.pixelNumber];
        
        RealNumber = PilotRealY * numpy.cos(2 * numpy.pi * self.CarrierFc * PilotModulateXData);
        ImageNumber = PilotImageY * numpy.sin(2 * numpy.pi * self.CarrierFc * PilotModulateXData);
        PilotModulateYData = RealNumber + ImageNumber;
        
        return PilotModulateXData, PilotModulateYData;
        
    def DeModulatePilotRealImageData(self, PilotModulateXData, PilotModulateYData):
        PilotDeModRealYData = PilotModulateYData * numpy.cos(2 * numpy.pi * self.CarrierFc * PilotModulateXData);
        PilotDeModImageYData = PilotModulateYData * numpy.sin(2 * numpy.pi * self.CarrierFc * PilotModulateXData);        
        return PilotModulateXData, PilotDeModRealYData, PilotDeModImageYData;
        
    def ModulateUserRealImageData(self, ConUserReal, ConUserImage):
        UserModulateYData = [];
        
        UserModulateXData = numpy.arange(self.PulseNumberXLeft, 
                                          self.PulseNumberXRight, 
                                          1.0 / self.pixelNumber);
        UserRealY = ConUserReal[self.filter_right_x * self.pixelNumber : (self.PulseNumber +  self.filter_right_x) * self.pixelNumber];
        UserImageY = ConUserImage[self.filter_right_x * self.pixelNumber : (self.PulseNumber +  self.filter_right_x) * self.pixelNumber];

        RealNumber = UserRealY * numpy.cos(2 * numpy.pi * self.CarrierFc * UserModulateXData);
        ImageNumber = UserImageY * numpy.sin(2 * numpy.pi * self.CarrierFc * UserModulateXData);
        UserModulateYData = RealNumber + ImageNumber;
        return UserModulateXData, UserModulateYData;
        
    def ModulatePilotAndUserData(self, PilotModulateYData, UserModulateYData):
        PilotAndUserYData = [];
        PilotAndUserXData = numpy.arange(self.PulseNumberXLeft - self.PilotNumber / 2, 
                                          self.PulseNumberXRight + self.PilotNumber / 2, 
                                          1.0 / self.pixelNumber);
                                          
        for i in range(len(PilotModulateYData)):
            PilotAndUserYData.append(PilotModulateYData[i]);
            
        for i in range(len(UserModulateYData)):
            PilotAndUserYData.append(UserModulateYData[i]);

        return PilotAndUserXData, PilotAndUserYData;
        
    def DeModulateUserRealImageData(self, UserModulateXData, UserModulateYData):
        UserDeModRealYData = UserModulateYData * numpy.cos(2 * numpy.pi * self.CarrierFc * UserModulateXData);
        UserDeModImageYData = UserModulateYData * numpy.sin(2 * numpy.pi * self.CarrierFc * UserModulateXData);        
        return UserModulateXData, UserDeModRealYData, UserDeModImageYData;
        
    def CombineRealImageData(self, ConPilotRealYArray, ConPilotImageYArray, ConUserRealYArray, ConUserImageYArray):
        PilotUserRealData = [];
        PilotUserImageData = [];
        PilotUserComplexData = [];
        
        PilotUserComplexX = numpy.arange(self.PulseNumberXLeft - self.PilotNumber / 2, 
                                          self.PulseNumberXRight + self.PilotNumber / 2, 
                                          1.0 / self.pixelNumber);
                                          
        PilotRealY = ConPilotRealYArray[self.filter_right_x * self.pixelNumber : (self.PilotNumber +  self.filter_right_x) * self.pixelNumber];
        PilotImageY = ConPilotImageYArray[self.filter_right_x * self.pixelNumber : (self.PilotNumber +  self.filter_right_x) * self.pixelNumber];
        
        UserRealY = ConUserRealYArray[self.filter_right_x * self.pixelNumber : (self.PulseNumber +  self.filter_right_x) * self.pixelNumber];
        UserImageY = ConUserImageYArray[self.filter_right_x * self.pixelNumber : (self.PulseNumber +  self.filter_right_x) * self.pixelNumber];
        
        for i in range(len(PilotRealY)):
            PilotUserRealData.append(PilotRealY[i]);
            
        for i in range(len(UserRealY)):
            PilotUserRealData.append(UserRealY[i]);
            
        for i in range(len(PilotImageY)):
            PilotUserImageData.append(PilotImageY[i]);
            
        for i in range(len(UserImageY)):
            PilotUserImageData.append(UserImageY[i]);
            
        for i in range(len(PilotUserRealData)):
            PilotUserComplexData.append(complex(PilotUserRealData[i], PilotUserImageData[i]));
            
        return UserRealY, UserImageY, PilotUserComplexData;
        #return PilotUserComplexX, PilotUserRealData, PilotUserImageData, PilotUserComplexData;
        
    def PilotUserComplexDataForChannel(self):
        PilotXArray, PilotBinaryData, PilotRealArray, PilotImageArray = self.GetPilotRealImageArray();
        UserXArray, UserBinaryData, UserRealArray, UserImageArray = self.GetUserRealImageArray();
        self.GetRaisedCosineArray();
        ConPilotRealXArray, ConPilotRealYArray, ConPilotImageXArray, ConPilotImageYArray = self.ConvolvePilotRealImageData(
                                    PilotRealArray, PilotImageArray, self.RaisedCosineYArray);
        ConUserRealXArray, ConUserRealYArray, ConUserImageXArray, ConUserImageYArray = self.ConvolveUserRealImageData(
                                    UserRealArray, UserImageArray, self.RaisedCosineYArray);
                                          
        UserRealY, UserImageY, PilotUserComplexData = self.CombineRealImageData(ConPilotRealYArray, ConPilotImageYArray, ConUserRealYArray, ConUserImageYArray);        
        
        return UserBinaryData, UserRealY, UserImageY, PilotUserComplexData;
    
    def BinaryJudgement(self, ReceivedRealData, ReceivedImageData, UserBinaryData):
        RealBinaryData = [];        
        ImageBinaryData = [];
        CombineBinaryData = [];
        #print len(ReceivedRealData);
        #print len(ReceivedImageData);
        for i in range(0, len(ReceivedRealData), self.pixelNumber):
            if (ReceivedRealData[i] > 0):
                RealBinaryData.append(1);
            else:
                RealBinaryData.append(0);
                
        for i in range(0, len(ReceivedImageData), self.pixelNumber):
            if (ReceivedImageData[i] > 0):
                ImageBinaryData.append(1);
            else:
                ImageBinaryData.append(0);
                
        #print len(RealBinaryData);
        #print len(ImageBinaryData);
        
        for i in range(len(RealBinaryData)):
            CombineBinaryData.append(RealBinaryData[i]);
            CombineBinaryData.append(ImageBinaryData[i]);
            
        #print len(UserBinaryData);
        #print len(CombineBinaryData);
        
        counter = 0;
        for i in range(len(UserBinaryData)):
            if (UserBinaryData[i] != CombineBinaryData[i]):
                counter = counter + 1;
                
        #print counter;
        #print float(counter) / self.PulseNumber;
        #print 4.0 / self.PulseNumber;
        
    def CreatePilotUserDataForChannel(self):
        PilotXArray, PilotBinaryData, PilotRealArray, PilotImageArray = self.GetPilotRealImageArray();
        UserXArray, UserBinaryData, UserRealArray, UserImageArray = self.GetUserRealImageArray();
        self.GetRaisedCosineArray();
        ConPilotRealXArray, ConPilotRealYArray, ConPilotImageXArray, ConPilotImageYArray = self.ConvolvePilotRealImageData(
                                    PilotRealArray, PilotImageArray, self.RaisedCosineYArray);
        ConUserRealXArray, ConUserRealYArray, ConUserImageXArray, ConUserImageYArray = self.ConvolveUserRealImageData(
                                    UserRealArray, UserImageArray, self.RaisedCosineYArray);
        PilotModulateXData, PilotModulateYData = self.ModulatePilotRealImageData(ConPilotRealYArray, 
                                                                                 ConPilotImageYArray);
        UserModulateXData, UserModulateYData = self.ModulateUserRealImageData(ConUserRealYArray, 
                                                                              ConUserImageYArray);
        
        PilotAndUserXData, PilotAndUserYData = self.ModulatePilotAndUserData(PilotModulateYData, UserModulateYData);
        
        return PilotAndUserXData, PilotAndUserYData;
        
    def DeModPilotUserData(self, PilotAndUserXData, PilotAndUserYData):
        DeModPilotUserRealData = PilotAndUserYData * numpy.cos(2 * numpy.pi * self.CarrierFc * PilotAndUserXData);
        DeModPilotUserImageData = PilotAndUserYData * numpy.sin(2 * numpy.pi * self.CarrierFc * PilotAndUserXData);
        return PilotAndUserXData, DeModPilotUserRealData, DeModPilotUserImageData;
        
    def ShowComplexData(self):
        PilotXArray, PilotRealArray, PilotImageArray = self.GetPilotRealImageArray();
        UserXArray, UserRealArray, UserImageArray = self.GetUserRealImageArray();
        self.GetRaisedCosineArray();
        ConPilotRealXArray, ConPilotRealYArray, ConPilotImageXArray, ConPilotImageYArray = self.ConvolvePilotRealImageData(
                                    PilotRealArray, PilotImageArray, self.RaisedCosineYArray);
        ConUserRealXArray, ConUserRealYArray, ConUserImageXArray, ConUserImageYArray = self.ConvolveUserRealImageData(
                                    UserRealArray, UserImageArray, self.RaisedCosineYArray);
                                          
        
        PilotUserComplexX, PilotUserRealData, PilotUserImageData, PilotUserComplexData = self.CombineRealImageData(ConPilotRealYArray, ConPilotImageYArray, ConUserRealYArray, ConUserImageYArray);        
        
        pylab.subplot(611);
        pylab.plot(ConPilotRealXArray, ConPilotRealYArray);
        pylab.grid('on')
        
        pylab.subplot(612);
        pylab.plot(ConPilotRealXArray, ConPilotImageYArray);
        pylab.grid('on')
        
        pylab.subplot(613);
        pylab.plot(ConUserRealXArray, ConUserRealYArray);
        pylab.grid('on')
        
        pylab.subplot(614);
        pylab.plot(ConUserRealXArray, ConUserImageYArray);
        pylab.grid('on')
        
        pylab.subplot(615);
        pylab.plot(PilotUserComplexX, PilotUserRealData);
        pylab.grid('on')
        
        pylab.subplot(616);
        pylab.plot(PilotUserComplexX, PilotUserImageData);
        pylab.grid('on')
    
    def ShowDeAndModulateData(self):
        PilotXArray, PilotRealArray, PilotImageArray = self.GetPilotRealImageArray();
        UserXArray, UserRealArray, UserImageArray = self.GetUserRealImageArray();
        self.GetRaisedCosineArray();
        ConPilotRealXArray, ConPilotRealYArray, ConPilotImageXArray, ConPilotImageYArray = self.ConvolvePilotRealImageData(
                                    PilotRealArray, PilotImageArray, self.RaisedCosineYArray);
        ConUserRealXArray, ConUserRealYArray, ConUserImageXArray, ConUserImageYArray = self.ConvolveUserRealImageData(
                                    UserRealArray, UserImageArray, self.RaisedCosineYArray);
        PilotModulateXData, PilotModulateYData = self.ModulatePilotRealImageData(ConPilotRealYArray, 
                                                                                 ConPilotImageYArray);
        UserModulateXData, UserModulateYData = self.ModulateUserRealImageData(ConUserRealYArray, 
                                                                              ConUserImageYArray);
        
        PilotAndUserXData, PilotAndUserYData = self.ModulatePilotAndUserData(PilotModulateYData, UserModulateYData);
        PilotAndUserXData, DeModPilotUserRealData, DeModPilotUserImageData = self.DeModPilotUserData(PilotAndUserXData, PilotAndUserYData);        
        pylab.subplot(511);
        pylab.plot(PilotModulateXData, PilotModulateYData);
        pylab.grid('on')
        
        pylab.subplot(512);
        pylab.plot(UserModulateXData, UserModulateYData);
        pylab.grid('on')
        
        pylab.subplot(513);
        pylab.plot(PilotAndUserXData, PilotAndUserYData);
        pylab.grid('on')
        
        pylab.subplot(514);
        pylab.plot(PilotAndUserXData, DeModPilotUserRealData);
        pylab.grid('on')
        
        pylab.subplot(515);
        pylab.plot(PilotAndUserXData, DeModPilotUserImageData);
        pylab.grid('on')
        
    def ShowAllPilotData(self):
        PilotModulateXData, PilotModulateYData = self.ModulatePilotRealImageData();
        PilotModulateXData, PilotDeModRealYData, PilotDeModImageYData = self.DeModulatePilotRealImageData(PilotModulateXData, PilotModulateYData);
        pylab.subplot(411);
        pylab.plot(self.ConPilotRealXArray, self.ConPilotRealYArray);
        pylab.grid('on')
        
        pylab.subplot(412);
        pylab.plot(self.ConPilotImageXArray, self.ConPilotImageYArray);
        pylab.grid('on');
        
        pylab.subplot(413);
        pylab.plot(PilotModulateXData, PilotDeModRealYData);
        pylab.grid('on')
        
        pylab.subplot(414);
        pylab.plot(PilotModulateXData, PilotDeModImageYData);
        pylab.grid('on')
        '''
        pylab.subplot(413);
        pylab.plot(self.PilotRealXArray, self.PilotRealArray);
        pylab.grid('on')
        
        pylab.subplot(414);
        pylab.plot(self.PilotImageXArray, self.PilotImageArray);
        pylab.grid('on');
        '''

    def QPSKBinaryNumber(self):
        PilotData = self.CreateQPSKPilotData();
        self.PilotLength = len(PilotData);
        UserData = [];
        for i in range(self.PulseNumber * 2):
            UserData.append(random.randint(0, 1));
            
        PilotAndUserData = PilotData + UserData;
        return PilotAndUserData;    

    def QPSKRealImageArray(self, randomNumber):
        RealArray = [];
        ImageArray = [];
        ArrayLength = 0;
        if (len(randomNumber) % 2 == 1):
            ArrayLength = len(randomNumber) - 1;
        elif (len(randomNumber) % 2 == 0):
            ArrayLength = len(randomNumber);
            
        for i in range(0, ArrayLength, 2):
            CurrentData = randomNumber[i] * 2 + randomNumber[i + 1];
            if (CurrentData == 0):
                RealNumber = -1;
                ImageNumber = -1;
            elif (CurrentData == 1):
                RealNumber = -1;
                ImageNumber = 1;
            elif (CurrentData == 2):
                RealNumber = 1;
                ImageNumber = -1;
            elif (CurrentData == 3):
                RealNumber = 1;
                ImageNumber = 1;
                
            for j in range(1):
                RealArray.append(RealNumber);
                ImageArray.append(ImageNumber);
            for j in range(1, self.pixelNumber):
                RealArray.append(0);
                ImageArray.append(0);                
                
        return RealArray, ImageArray;    
        
if __name__ == '__main__':
    ImpulseObject = ImpulseForming(50, 50, 100, -4, 4, 0.5, 5);
    #ImpulseObject.ShowDeAndModulateData();
    #ImpulseObject.PilotUserComplexDataForChannel();
    #ImpulseObject.ShowComplexData();
    UserBinaryData, ConUserRealYArray, ConUserImageYArray, PilotUserComplexData = ImpulseObject.PilotUserComplexDataForChannel();
    ImpulseObject.BinaryJudgement(ConUserRealYArray, ConUserImageYArray, UserBinaryData);