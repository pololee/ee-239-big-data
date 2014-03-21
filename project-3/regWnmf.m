function [X,Y,tElapsed]=regWnmf(R,W,f,lambda,option)
% Weighted NMF based on multiple update rules for missing values: X=AY, s.t. A,Y>=0.
% Definition:
%     [A,Y,numIter,tElapsed,finalResidual]=wnmfrule(X,k)
%     [A,Y,numIter,tElapsed,finalResidual]=wnmfrule(X,k,option)
% X: non-negative matrix, dataset to factorize, each column is a sample,
% and each row is a feature. A missing value is represented by NaN.
% k: number of clusters.
% option: struct:
% option.distance: distance used in the objective function. It could be
%    'ls': the Euclidean distance (defalut),
%    'kl': KL divergence.
% option.iter: max number of interations. The default is 1000.
% option.dis: boolen scalar, It could be 
%     false: not display information,
%     true: display (default).
% option.residual: the threshold of the fitting residual to terminate. 
%    If the ||X-XfitThis||<=option.residual, then halt. The default is 1e-4.
% option.tof: if ||XfitPrevious-XfitThis||<=option.tof, then halt. The default is 1e-4.
% A: matrix, the basis matrix.
% Y: matrix, the coefficient matrix.
% numIter: scalar, the number of iterations.
% tElapsed: scalar, the computing time used.
% finalResidual: scalar, the fitting residual.


tStart=tic;
optionDefault.iter=1000;
optionDefault.dis=true;
optionDefault.residual=1e-4;
optionDefault.tof=1e-4;
if nargin<5
   option=optionDefault;
else
    option=mergeOption(option,optionDefault);
end

%%%%%%
%% we want to get R = X*Y'
%% size(R) = [m,n]
%% size(X) = [m,f]
%% size(Y) = [n,f]
%%%%

% iter: number of iterations
[m,n]=size(R); % m is # of users, n is # of movies

% initiate Y with random values
Y=rand(n,f);
% Y(Y<eps)=0;
Y=max(Y,eps);

X = zeros(m,f);

RfitPrevious=Inf;

for it=1:option.iter
    tmpY = Y'*Y;
    for u=1:m
        Cu = diag(W(u,:));
        pu = R(u,:)';
        xu = (tmpY + (Y'*(Cu-eye(n))*Y) + lambda.*eye(f))^(-1)*Y'*Cu*pu;
        X(u,:)=xu';
    end
    X = max(X,eps);
    tmpX = X'*X;
    for i=1:n
        Ci = diag(W(:,i));
        pi = R(:,i);
        yi = (tmpX + X'*(Ci-eye(m))*X + lambda.*eye(f))^(-1)*X'*Ci*pi;
        Y(i,:) = yi';
    end
    Y = max(Y,eps);
    if mod(it,10)==0 || it==option.iter
        if option.dis
            disp(['Iterating >>>>>> ', num2str(it),'th']);
        end
        RfitThis=X*Y';
        fitRes=matrixNorm(W.*(RfitPrevious-RfitThis));
        RfitPrevious=RfitThis;
        curRes=norm(W.*(R-RfitThis),'fro');
        if option.tof>=fitRes || option.residual>=curRes || it==option.iter
            s=sprintf('Mutiple update rules based NMF successes! \n # of iterations is %0.0d. \n The final residual is %0.4d.',it,curRes);
            disp(s);
            numIter=it;
            finalResidual=curRes;
            break;
        end
    end
end
Y = Y';
tElapsed=toc(tStart);
end